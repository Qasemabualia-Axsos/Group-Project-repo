from django.urls import path
from .api_views import DirectorListCreateAPI, DirectorDetailAPI

urlpatterns = [
    path("", DirectorListCreateAPI.as_view(), name="api_director_list"),
    path("<int:pk>/", DirectorDetailAPI.as_view(), name="api_director_detail"),
]
