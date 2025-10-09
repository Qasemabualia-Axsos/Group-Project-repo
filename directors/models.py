# directors/models.py
from django.db import models
from django.core.validators import FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_image_size(image):
    max_mb = 3
    if image and image.size > max_mb * 1024 * 1024:
        raise ValidationError(f"Image size exceeds {max_mb} MB.")

class Director(models.Model):
    name = models.CharField(
        max_length=80,
        help_text="Director's name (public).",
        validators=[
            RegexValidator(regex=r"^[^\d]+$", message="Name should not contain digits.")
        ],
    )
    bio = models.TextField(blank=True, default="", help_text="Short biography.")
    profile_img = models.ImageField(
        upload_to="directors/",
        blank=True,
        validators=[FileExtensionValidator(['jpg','jpeg','png','webp']), validate_image_size],
        help_text="JPG/PNG/WEBP ≤ 3MB"
    )

    # Optional helpers
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=60, blank=True, default="")
    website = models.URLField(blank=True, default="")
    imdb_url = models.URLField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # بس ترتيب، بدون قيود معقدة

    def clean(self):
        if self.date_of_birth and self.date_of_birth > timezone.localdate():
            raise ValidationError({"date_of_birth": "Birth date cannot be in the future."})
        if self.imdb_url and "imdb.com" not in self.imdb_url.lower():
            raise ValidationError({"imdb_url": "IMDb URL must come from imdb.com."})

    def __str__(self):
        return self.name
