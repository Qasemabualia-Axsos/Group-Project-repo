from django.db import models
from actors.models import Actor
from directors.models import Director

class Movie(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField(max_length=400)
    release_date = models.DateField()
    trailer = models.URLField()
    cover_img = models.ImageField(upload_to='covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    actors = models.ManyToManyField(Actor, related_name="movies")
    directors = models.ManyToManyField(Director, related_name="movies")

    def __str__(self):
        return self.title
