from django.db import models

# Create your models here.
from django.db import models


class Review(models.Model):
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey('movies.Movies', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return f"{self.movie.title} ({self.rating}/5)"