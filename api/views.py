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

# Create your views here.

load_dotenv()
def api(request):
    # === Local DB data ===
    movies = Movies.objects.all()
    actors = Actor.objects.all()
    directors = Director.objects.all()
    top_movies = Movies.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]

    # === TMDb API for upcoming movies ===
    api_key = os.getenv("TMDB_API_KEY", "2cdda5a49ba08a74a18ca8712545b251")  # fallback for testing
    url = "https://api.themoviedb.org/3/movie/upcoming"
    params = {
        "api_key": api_key,
        "language": "en-US",
        "region": "US",
        "page": 1
    }

    upcoming_movies = []

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for movie in data.get("results", []):
            poster_url = (
                f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                if movie.get("poster_path") else
                "https://via.placeholder.com/200x300?text=No+Image"
            )

            upcoming_movies.append({
                "title": movie.get("title"),
                "poster": poster_url,
                "release_date": movie.get("release_date"),
            })

    except requests.exceptions.RequestException as e:
        print("Error fetching TMDb upcoming movies:", e)

    # === Context for template ===
    context = {
        "Movies": movies,
        "Actors": actors,
        "Directors": directors,
        "top_movies": top_movies,
        "upcoming_movies": upcoming_movies,
    }

    return render(request, "api.html", context)