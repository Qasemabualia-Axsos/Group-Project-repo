from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to="directors/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
