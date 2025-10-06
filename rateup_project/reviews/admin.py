from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "rating", "created_at")
    search_fields = ("movie__title", "user__username", "comment")
    list_filter = ("rating", "created_at")
