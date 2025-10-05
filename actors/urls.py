from django.urls import path
from . import views

app_name = "actors"

urlpatterns = [
    path("", views.actor_list, name="actor_list"),
    path("<int:actor_id>/", views.actor_detail, name="actor_detail"),
    path("create/", views.actor_create, name="actor_create"),
    path("<int:actor_id>/edit/", views.actor_update, name="actor_update"),
    path("<int:actor_id>/delete/", views.actor_delete, name="actor_delete"),
    path("api/", views.actor_api, name="actor_api"),
]
