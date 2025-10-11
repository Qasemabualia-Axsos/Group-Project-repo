from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=45)
    bio = models.TextField(blank=True, default="")  # safer: avoids migration errors when DB already has NULLs
    profile_img = models.ImageField(upload_to="directors/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
