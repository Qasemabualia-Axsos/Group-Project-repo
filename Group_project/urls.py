"""
URL configuration for Group_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage → Movies
    path('', include('movies.urls')),

    # Accounts app
    path('accounts/', include('accounts.urls')),

    # Reviews app
    path('reviews/', include('reviews.urls')),

    # Actors app
    path('actors/', include('actors.urls')),

    # Directors app
    path('directors/', include('directors.urls')),

    # Categories app
    path('categories/', include('categories.urls')),

    # API app
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
