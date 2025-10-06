from django.urls import path
from .api_views import ReviewListCreateAPI, ReviewDetailAPI

urlpatterns = [
    path("movie/<int:movie_id>/", ReviewListCreateAPI.as_view(), name="api_reviews"),
    path("<int:pk>/", ReviewDetailAPI.as_view(), name="api_review_detail"),
]
