from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("movie/<int:movie_id>/add/", views.add_review, name="add_review"),
    path("<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("<int:review_id>/delete/", views.delete_review, name="delete_review"),
]
