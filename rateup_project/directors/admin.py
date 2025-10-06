from django.contrib import admin
from .models import Director

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
