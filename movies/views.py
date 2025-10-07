from django.shortcuts import render,redirect,HttpResponse
from .models import Actor,Director,Movies
from accounts.models import *
from actors.models import *
from directors.models import *
from django.http import JsonResponse
from django.db.models import Avg, Count
from reviews.models import *


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


def view_movie(request,movie_id):
    if 'userid' not in request.session:
        return redirect('accounts:login_page')

    # Filter and get the first matching movie (or None)
    movie = Movies.objects.filter(id=movie_id).first()
    if not movie:
        return HttpResponse("Movie not found", status=404)

    actors = movie.actors.all()
    directors = movie.directors.all()

    data = {
        'movie': movie,
        'actors': actors,
        'directors': directors
    }
    return render (request,'movie.html',data)

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