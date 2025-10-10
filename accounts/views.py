from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import requests, os
from dotenv import load_dotenv

# Models
from .models import Users
from movies.models import Movies
from actors.models import Actor
from directors.models import Director
from categories.models import Category
from reviews.models import Review

load_dotenv()


# ===================== HOME PAGE ===================== #
def home(request):
    # Featured movies (random 8)
    featured_movies = Movies.objects.order_by('?')[:8]

    # Trending (by number of reviews)
    trending_movies = Movies.objects.annotate(
        review_count=Count('reviews')
    ).order_by('-review_count')[:8]

    # Categories, Actors, Directors
    categories = Category.objects.all()
    top_actors = Actor.objects.all()[:6]
    top_directors = Director.objects.all()[:6]

    # Latest reviews
    latest_reviews = Review.objects.select_related('movie', 'user').order_by('-created_at')[:5]

    # Upcoming (from DB release date)
    upcoming_movies = Movies.objects.filter(release_date__gte=timezone.now())[:8]

    # RapidAPI Upcoming (optional extra)
    rapidapi_movies = []
    url = "https://upcoming-releases-movies.p.rapidapi.com/api/movie/upcoming/us"
    headers = {
        "x-rapidapi-host": "upcoming-releases-movies.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY", "")
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            rapidapi_movies = response.json()
    except Exception as e:
        print("⚠️ Error fetching RapidAPI movies:", e)

    return render(request, "index.html", {
        "featured_movies": featured_movies,
        "trending_movies": trending_movies,
        "categories": categories,
        "top_actors": top_actors,
        "top_directors": top_directors,
        "latest_reviews": latest_reviews,
        "upcoming_movies": upcoming_movies if upcoming_movies else rapidapi_movies,
    })


# ===================== AUTH ===================== #
def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Users.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            # Set session
            request.session['userid'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, 'Logged in successfully!', extra_tags='login')
            return redirect('movies:dashboard')

        messages.error(request, 'Invalid email or password', extra_tags='login')
        return redirect('accounts:login_page')
    return redirect('accounts:login_page')


def register(request):
    if request.method == 'POST':
        errors = Users.objects.user_validator(request.POST)
        if errors:
            for field, error in errors.items():
                messages.error(request, error, extra_tags=field)
            return redirect('accounts:register_page')

        user = Users.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=make_password(request.POST['password'])  # ✅ Always hashed
        )

        request.session['userid'] = user.id
        request.session['first_name'] = user.first_name
        messages.success(request, 'Account created successfully!', extra_tags='register')
        return redirect('movies:dashboard')

    return render(request, 'register.html')


# ===================== PROFILE ===================== #
def user_profile(request):
    if 'userid' not in request.session:
        return redirect('accounts:login_page')
    user = Users.objects.get(id=request.session['userid'])
    return render(request, 'user_profile.html', {'user': user})


def edit_profile(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = Users.objects.get(id=request.session['userid'])
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()

        return JsonResponse({
            "status": "success",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        })
    return JsonResponse({"status": "failed", "message": "Invalid request"})


@login_required
def delete_profile(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = Users.objects.get(id=request.session['userid'])
        user.delete()
        request.session.flush()  # clear session
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed", "message": "Invalid request"})
