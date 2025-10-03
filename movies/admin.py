from django.contrib import admin
from .models import Movie

# Custom Admin for Movies
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("release_date", "created_at")
    filter_horizontal = ("actors", "directors")  # nice UI for ManyToMany fields
    ordering = ("-release_date",)
