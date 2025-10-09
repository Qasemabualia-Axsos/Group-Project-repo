# directors/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Director

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "nationality", "is_active", "created_at")
    list_filter = ("is_active", "nationality", "created_at")
    search_fields = ("name", "nationality")
    # احذف أي ذكر لـ 'slug' هنا
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def thumb(self, obj):
        if obj.profile_img:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;object-fit:cover;" />',
                obj.profile_img.url
            )
        return "—"
    thumb.short_description = "Image"
