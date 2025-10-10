from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.dashboard, name='home'),  # root URL shows dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('view_movie/<int:movie_id>', views.view_movie, name='view_movie'),
    path('ajax-search/', views.ajax_search_movies, name='ajax_search_movies'),
    path('about/', views.about, name='about'),  # Added a about us page
    path('contact/', views.contact, name='contact'),  #  added a contact us page 
]
