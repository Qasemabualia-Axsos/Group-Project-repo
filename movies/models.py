from django.db import models

# Create your models here.
class Actors(models.Model):
    name=models.CharField(max_length=45)
    bio=models.TextField()
    profile_img=models.ImageField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"

class Directors(models.Model):
    name=models.CharField(max_length=45)
    bio=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
class Movies(models.Model):
    title=models.CharField(max_length=45)
    description=models.TextField(max_length=400)
    release_date=models.DateField()
    trailer=models.URLField()
    cover_img=models.ImageField(upload_to='covers/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    actors=models.ManyToManyField(Actors,related_name='movies')
    directors=models.ManyToManyField(Directors,related_name='movies')

    def __str__(self):
        return f'{self.title}'