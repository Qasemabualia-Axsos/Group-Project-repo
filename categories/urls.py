from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('', views.categories_page, name='page'), 
    # API (AJAX/JSON)
    path('api/list/', views.api_list, name='api_list'),
    path('api/create/', views.api_create, name='api_create'),
    path('api/update/<int:pk>/', views.api_update, name='api_update'),
    path('api/delete/<int:pk>/', views.api_delete, name='api_delete'),
]
