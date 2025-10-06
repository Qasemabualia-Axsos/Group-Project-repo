from django.urls import path
from . import views

app_name = "actors"

urlpatterns = [
    path("", views.actor_list, name="actor_list"),
    path("<int:pk>/", views.actor_detail, name="actor_detail"),
    path("create/", views.actor_create, name="actor_create"),
    path("<int:pk>/edit/", views.actor_update, name="actor_update"),
    path("<int:pk>/delete/", views.actor_delete, name="actor_delete"),
]
