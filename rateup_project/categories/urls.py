from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    CategoryListAPI, CategoryDetailAPI
)

app_name = "categories"

urlpatterns = [
    # HTML
    path("", CategoryListView.as_view(), name="index"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="detail"),
    path("create/", CategoryCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete"),

    # API
    path("api/", CategoryListAPI.as_view(), name="api-list"),
    path("api/<int:pk>/", CategoryDetailAPI.as_view(), name="api-detail"),
]
