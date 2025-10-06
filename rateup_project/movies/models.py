from django.db import models
from categories.models import Category
from actors.models import Actor
from directors.models import Director

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    directors = models.ManyToManyField("directors.Director", related_name="movies")
    actors = models.ManyToManyField("actors.Actor", related_name="movies")
    categories = models.ManyToManyField("categories.Category", related_name="movies")


    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
