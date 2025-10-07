import os
import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from actors.models import Actor
from directors.models import Director
from categories.models import Category
from movies.models import Movies
from accounts.models import Users
from reviews.models import Review

fake = Faker()

MEDIA_COVERS = "media/covers"

class Command(BaseCommand):
    help = "Populate dummy data: actors, directors, categories, movies, users, reviews with dummy images"

    def handle(self, *args, **kwargs):
        # Ensure covers folder exists
        os.makedirs(MEDIA_COVERS, exist_ok=True)

        # --- Actors ---
        actors = [Actor.objects.create(name=fake.name()) for _ in range(20)]

        # --- Directors ---
        directors = [Director.objects.create(name=fake.name()) for _ in range(10)]

        # --- Categories ---
        categories = []
        for cat_name in ["Action", "Drama", "Comedy", "Horror", "Sci-Fi", "Romance", "Thriller", "Fantasy"]:
            categories.append(Category.objects.create(name=cat_name))

        # --- Users ---
        users = []
        for _ in range(30):
            users.append(
                Users.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    password="password123"  # plaintext; hash manually if needed
                )
            )

        # --- Movies ---
        movies = []
        for i in range(100):  # <-- 100 movies
            # Create dummy cover image
            img = Image.new('RGB', (400, 600), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            image_file = ContentFile(buffer.getvalue(), name=f"cover_{i}.jpg")

            movie = Movies.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=200),
                release_date=fake.date_this_century(),
                trailer="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                cover_img=image_file
            )

            # Add relations
            movie.actors.add(*random.sample(actors, k=random.randint(1,5)))
            movie.directors.add(*random.sample(directors, k=random.randint(1,2)))
            movie.categories.add(*random.sample(categories, k=random.randint(1,3)))

            movies.append(movie)

        # --- Reviews ---
        for movie in movies:
            for _ in range(random.randint(1,10)):  # random number of reviews per movie
                Review.objects.create(
                    user=random.choice(users),
                    movie=movie,
                    rating=random.randint(1,5),
                    comment=fake.text(max_nb_chars=150)
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated 100 movies with all related data!"))
