import os
import random
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from faker import Faker
from io import BytesIO

from actors.models import Actor
from directors.models import Director
from categories.models import Category
from movies.models import Movies
from accounts.models import Users
from reviews.models import Review

fake = Faker()

# --- Utility: Fetch random image from web (picsum.photos) ---
def fetch_random_image(width, height, name):
    url = f"https://picsum.photos/{width}/{height}?random={random.randint(1,10000)}"
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content, name=f"{name}.jpg")
    return None


class Command(BaseCommand):
    help = "🌱 Seed pro-level dummy data with real images for local testing"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding pro-level dummy data...")

        # --- Categories ---
        categories = []
        category_names = ["Action", "Drama", "Comedy", "Horror", "Sci-Fi", "Romance", "Thriller", "Fantasy"]
        for idx, cat_name in enumerate(category_names):
            image = fetch_random_image(600, 400, f"category_{idx}")
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    "description": fake.text(max_nb_chars=100),
                    "image": image
                }
            )
            categories.append(category)

        # --- Actors ---
        actors = []
        for i in range(20):
            name = fake.name()
            profile_img = fetch_random_image(300, 300, f"actor_{i}")
            actors.append(
                Actor.objects.create(
                    name=name,
                    bio=fake.text(max_nb_chars=250),
                    profile_img=profile_img,
                )
            )

        # --- Directors ---
        directors = []
        for i in range(10):
            name = fake.name()
            profile_img = fetch_random_image(300, 300, f"director_{i}")
            directors.append(
                Director.objects.create(
                    name=name,
                    bio=fake.text(max_nb_chars=250),
                    profile_img=profile_img,
                )
            )

        # --- Users ---
        users = []
        for _ in range(30):
            user, _ = Users.objects.get_or_create(
                email=fake.unique.email(),
                defaults={
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "password": make_password("password123"),
                },
            )
            users.append(user)

        # --- Movies ---
        movies = []
        for i in range(50):  # keep it light, 50 movies
            cover_img = fetch_random_image(400, 600, f"movie_{i}")
            movie = Movies.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=250),
                release_date=fake.date_between(start_date="-20y", end_date="+2y"),
                trailer="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                cover_img=cover_img,
            )
            movie.actors.add(*random.sample(actors, k=random.randint(1, 4)))
            movie.directors.add(*random.sample(directors, k=random.randint(1, 2)))
            movie.categories.add(*random.sample(categories, k=random.randint(1, 3)))
            movies.append(movie)

        # --- Reviews ---
        for movie in movies:
            for _ in range(random.randint(2, 5)):
                Review.objects.create(
                    user=random.choice(users),
                    movie=movie,
                    rating=random.randint(1, 5),
                    comment=fake.text(max_nb_chars=150),
                )

        self.stdout.write(self.style.SUCCESS("✅ Pro dummy data seeded with real images!"))
