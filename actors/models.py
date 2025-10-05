from django.db import models

class Actor(models.Model):
    name = models.CharField(max_length=45)
    bio = models.TextField(blank=True, default="")  # avoids migration issues
    profile_img = models.ImageField(upload_to="actors/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
