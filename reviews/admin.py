from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'movie')
    search_fields = ('movie__title', 'user__username', 'comment')
    ordering = ('-created_at',)