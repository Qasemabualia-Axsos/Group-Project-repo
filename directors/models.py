from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=45)
    bio = models.TextField(blank=True, default="")
    profile_img = models.ImageField(upload_to="directors/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]  # directors sorted alphabetically

    def __str__(self):
        return self.name
