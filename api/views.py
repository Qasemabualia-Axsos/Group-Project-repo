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
def api(request):
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

    return render(request, "api.html", context)