from django.urls import path
from . import views

app_name = 'reviews'  # 🔹 Important: allows namespacing like reviews:add_review

urlpatterns = [
    path('<int:movie_id>/', views.movie_reviews, name='movie_reviews'),
    path('<int:movie_id>/add/', views.movie_reviews, name='movie_reviews'),
    path('<int:movie_id>/edit/', views.movie_reviews, name='movie_reviews'),
    path('<int:movie_id>/delete/', views.movie_reviews, name='movie_reviews'),
    # path('<int:movie_id>/add/', views.add_review, name='add_review'),

    # path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    # path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
