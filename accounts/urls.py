from django.urls import path
from . import views
app_name='accounts'
urlpatterns = [
    path('',views.home,name='home'),
    path('login_page/',views.login_page,name='login_page'),
    path('register_page/',views.register_page,name='register_page'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact')

    
]
