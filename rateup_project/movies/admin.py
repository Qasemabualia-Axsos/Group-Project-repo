from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'rating')
    list_filter = ('categories', 'directors', 'release_date')
    search_fields = ('title', 'description')
    ordering = ('-release_date',)
    filter_horizontal = ('actors', 'categories', 'directors') 

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "description", "release_date", "poster")
        }),
        ("Relations", {
            "fields": ("categories", "directors", "actors")
        }),
        ("Ratings & Meta", {
            "fields": ("rating",)
        }),
    )
