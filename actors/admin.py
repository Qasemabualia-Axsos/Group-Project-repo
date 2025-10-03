from django.contrib import admin
from .models import Actor

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)
