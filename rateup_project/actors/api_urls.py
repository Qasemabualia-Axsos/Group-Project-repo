from django.urls import path
from .api_views import ActorListCreateAPI, ActorDetailAPI

urlpatterns = [
    path("", ActorListCreateAPI.as_view(), name="api_actor_list"),
    path("<int:pk>/", ActorDetailAPI.as_view(), name="api_actor_detail"),
]
