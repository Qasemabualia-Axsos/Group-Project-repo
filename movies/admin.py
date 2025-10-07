from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Actor, Director, Movies

# Custom Admin for Actors

# Custom Admin for Movies
@admin.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("release_date", "created_at")
    filter_horizontal = ("actors", "directors", "categories")  # Add categories here
    ordering = ("-release_date",)
