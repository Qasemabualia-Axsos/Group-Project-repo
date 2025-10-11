from django.shortcuts import render,redirect,HttpResponse
from .models import Actor,Director,Movies
from accounts.models import *
from actors.models import *
from directors.models import *
from django.http import JsonResponse
from django.db.models import Avg, Count
from reviews.models import *
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favorite
import random

API_KEY = "2cdda5a49ba08a74a18ca8712545b251"


# Create your views here.
def dashboard(request):
    if 'userid' not in request.session:
        return redirect('accounts:login_page')

    # All movies, actors, directors
    movies = Movies.objects.all()
    actors = Actor.objects.all()
    directors = Director.objects.all()

    # Top movies by average rating (top 5)
    top_movies = Movies.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]

    latest_reviews = Review.objects.select_related('movie', 'user').order_by('-created_at')[:5]


    context = {
        'Movies': movies,
        'Actors': actors,
        'Directors': directors,
        'top_movies': top_movies,
        'latest_reviews': latest_reviews
    }

    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect ('accounts:home')


def view_movie(request, movie_id):
    # Check login via session

    movie = get_object_or_404(Movies, id=movie_id)
    actors = movie.actors.all()
    directors = movie.directors.all()

    # Fetch user's favorite movies using session userid
    user_id = request.session.get('userid')
    user_favorites = Favorite.objects.filter(user_id=user_id).values_list('movie_id', flat=True)

    context = {
        'movie': movie,
        'actors': actors,
        'directors': directors,
        'user_favorites': list(user_favorites),  # convert queryset to list
    }

    return render(request, 'movie.html', context)
def top_movies(request):
    movies = Movies.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:10]  

    context = {
        'top_movies': movies
    }
    return render(request, 'top_movies.html', context)

def ajax_search_movies(request):
    query = request.GET.get('q', '')
    movies = Movies.objects.filter(title__icontains=query) if query else []
    results = []
    for movie in movies:
        results.append({
            'id': movie.id,
            'title': movie.title,
            'cover': movie.cover_img.url,
        })
    return JsonResponse({'movies': results})


def toggle_favorite(request, movie_id):
    if 'userid' not in request.session:
        return redirect('accounts:login_page')

    user_id = request.session.get('userid')
    movie = get_object_or_404(Movies, id=movie_id)

    favorite, created = Favorite.objects.get_or_create(user_id=user_id, movie=movie)
    if not created:
        favorite.delete()  # remove if already exists

    return redirect(request.META.get('HTTP_REFERER', '/'))



def random_movie(request):
    movies = Movies.objects.all()
    if movies.exists():
        random_movie = random.choice(movies)
        return redirect('movies:view_movie', movie_id=random_movie.id)
    else:
        # If no movies exist, redirect to dashboard or show message
        return redirect('movies:dashboard')