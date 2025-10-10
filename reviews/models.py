from django.db import models


class Review(models.Model):
    # Correctly reference your Users model in accounts
    user = models.ForeignKey(
        'accounts.Users',        # points to class Users in accounts/models.py
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    # Reference Movies model
    movie = models.ForeignKey(
        'movies.Movies',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField()  # safer: only positive 1-5
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie.title} ({self.rating}/5)"
