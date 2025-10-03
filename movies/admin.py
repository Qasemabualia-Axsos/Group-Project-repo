from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Actors, Directors, Movies

# Custom Admin for Actors
@admin.register(Actors)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

# Custom Admin for Directors
@admin.register(Directors)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

# Custom Admin for Movies
@admin.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("release_date", "created_at")
    filter_horizontal = ("actors", "directors")  # nice UI for ManyToMany fields
    ordering = ("-release_date",)
