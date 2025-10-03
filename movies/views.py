from django.shortcuts import render,redirect,HttpResponse
from .models import *
from accounts.models import *
# Create your views here.

def dashboard(request):
    if 'userid' not in request.session:
        return redirect('login_page')
    movie=Movie.objects.all()
    actor=Actor.objects.all()
    director=Director.objects.all()
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
    movie = Movie.objects.filter(id=movie_id).first()
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