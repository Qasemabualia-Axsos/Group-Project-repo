from django.db import models
from actors.models import Actor
from directors.models import Director
from categories.models import Category
from accounts.models import Users
# Create your models here.

    
class Movies(models.Model):
    title=models.CharField(max_length=45)
    description=models.TextField(max_length=400)
    release_date=models.DateField()
    trailer=models.URLField()
    cover_img=models.ImageField(upload_to='covers/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    actors=models.ManyToManyField(Actor,related_name='movies')
    directors=models.ManyToManyField(Director,related_name='movies')
    categories = models.ManyToManyField(Category, related_name='movies')

    def __str__(self):
        return f'{self.title} {self.release_date}'
    

class Favorite(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # prevent duplicates

    def __str__(self):
        return f"{self.user.first_name} - {self.movie.title}"