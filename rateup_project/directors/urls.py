from django.urls import path
from . import views

app_name = "directors"

urlpatterns = [
    path("", views.director_list, name="director_list"),
    path("<int:pk>/", views.director_detail, name="director_detail"),
    path("create/", views.director_create, name="director_create"),
    path("<int:pk>/edit/", views.director_update, name="director_update"),
    path("<int:pk>/delete/", views.director_delete, name="director_delete"),
]
