# movies/urls.py
from django.urls import path
from .views import (
    MovieListView, MovieDetailView, MovieCreateView,
    MovieUpdateView, MovieDeleteView, MovieListAPI, MovieDetailAPI
)

app_name = "movies"

urlpatterns = [
    path("", MovieListView.as_view(), name="movie_list"),
    path("<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("create/", MovieCreateView.as_view(), name="movie_create"),
    path("<int:pk>/edit/", MovieUpdateView.as_view(), name="movie_edit"),
    path("<int:pk>/delete/", MovieDeleteView.as_view(), name="movie_delete"),

    # API
    path("api/", MovieListAPI.as_view(), name="movie_api_list"),
    path("api/<int:pk>/", MovieDetailAPI.as_view(), name="movie_api_detail"),
]
