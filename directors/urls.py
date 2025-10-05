from django.urls import path
from . import views

app_name = "directors"

urlpatterns = [
    path("", views.director_list, name="director_list"),
    path("<int:director_id>/", views.director_detail, name="director_detail"),
    path("create/", views.director_create, name="director_create"),
    path("<int:director_id>/edit/", views.director_update, name="director_update"),
    path("<int:director_id>/delete/", views.director_delete, name="director_delete"),
    path("api/", views.director_api, name="director_api"),
]
