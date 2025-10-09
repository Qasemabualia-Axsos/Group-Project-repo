from django.shortcuts import render,redirect
from .models import *
import os
from django.contrib import messages
from movies.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
import requests
from dotenv import load_dotenv
import datetime

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # Make sure your .env has:
# OMDB_API_KEY=929ac58b-7412-4c90-b63f-94d769831462

import requests

def home(request):
    # Local DB data
    movies = Movies.objects.all()
    actors = Actor.objects.all()
    directors = Director.objects.all()
    top_movies = Movies.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]

    # Fetch upcoming movies from RapidAPI
    upcoming_movies = []
    url = "https://upcoming-releases-movies.p.rapidapi.com/api/movie/upcoming/us"
    headers = {
        "x-rapidapi-host": "upcoming-releases-movies.p.rapidapi.com",
        "x-rapidapi-key": "f88ebd443amsh0623ee9d3f6e39ap1b4552jsn0daa5643fe2f"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        upcoming_movies = response.json()  # ✅ keep the list
    except requests.exceptions.RequestException as e:
        print("Error fetching RapidAPI movies:", e)
        upcoming_movies = []  # only empty on error

    context = {
        "Movies": movies,
        "Actors": actors,
        "Directors": directors,
        "top_movies": top_movies,
        "upcoming_movies": upcoming_movies,
    }

    return render(request, "home.html", context)


def login_page(request):
    return render (request,'login.html')

def register_page(request):

    return render (request,'register.html')

def login(request):
    if request.method=='POST':
        user=Users.objects.filter(email=request.POST.get('email')).first()
        
        if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
                request.session['userid']=user.id
                request.session['first_name']=user.first_name
                request.session['last_name']=user.last_name
                messages.success(request, 'Logged in successfully!', extra_tags='login')
                return redirect('movies:dashboard')
        else:
            messages.error(request,'Invalid email or password',extra_tags='login')
            return redirect('accounts:login_page')
    return redirect('accounts:login_page')


def register(request):
    if request.method == 'POST':
        errors = Users.objects.user_validator(request.POST)
        if errors:
            for field, error in errors.items():
                messages.error(request, error, extra_tags=field)
            return redirect('accounts:register_page')

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = Users.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash
        )

        request.session['userid'] = user.id
        request.session['first_name'] = user.first_name
        messages.success(request, 'Account created successfully!', extra_tags='register')
        return redirect('movies:dashboard')

    return render(request, 'accounts:register_page')


def user_profile(request):
    if 'userid' not in request.session:
        return redirect('login_page')
    user=Users.objects.get(id=request.session['userid'])
    data={
        'user':user
    }
    return render (request,'user_profile.html',data)



def edit_profile(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = Users.objects.get(id=request.session['userid'])
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        if email: user.email = email

        user.save()
        # return updated data
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
