from django.shortcuts import render,redirect,HttpResponse
from .models import *
from accounts.models import *
from django.http import JsonResponse

# Create your views here.

def dashboard(request):
    if 'userid' not in request.session:
        return redirect('login_page')
    movie=Movies.objects.all()
    actor=Actors.objects.all()
    director=Directors.objects.all()
    data={
        'Movies':movie,
        'Actors':actor,
        'Directors':director
    }
    return render(request,'dashboard.html',data)

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