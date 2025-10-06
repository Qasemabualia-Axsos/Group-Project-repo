from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Movie
from .forms import MovieForm

# DRF
from rest_framework import generics
from .serializers import MovieSerializer

# ---------------- Web Views ----------------
class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    context_object_name = "movies"


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movies:movie_list")


class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_url = reverse_lazy("movies:movie_list")


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = "movies/movie_confirm_delete.html"
    success_url = reverse_lazy("movies:movie_list")


# ---------------- API Views ----------------
class MovieListAPI(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
