from django.urls import path
from . import views
app_name='movies'
urlpatterns = [
    # path('movie/<int:movie_id>',views.movie,name='movie'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout,name='logout'),
    path('view_movie/<int:movie_id>',views.view_movie,name='view_movie')
    
]
