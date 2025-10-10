from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Review
from movies.models import Movies
from accounts.models import Users

# List all reviews for a movie
def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    reviews = Review.objects.filter(movie=movie).select_related("user")

    return render(request, "reviews/movie_reviews.html", {
        "movie": movie,
        "reviews": reviews,
    })


# Add review
@require_POST
def add_review(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    user_id = request.session.get("userid")

    if not user_id:
        return JsonResponse({"success": False, "message": "Login required."}, status=403)

    comment = request.POST.get("comment")
    rating = request.POST.get("rating", 0)

    review = Review.objects.create(
        movie=movie,
        user_id=user_id,
        rating=rating,
        comment=comment,
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "id": review.id,
            "comment": review.comment,
            "rating": review.rating,
            "created_at": timezone.localtime(review.created_at).strftime("%b %d, %Y %H:%M"),
        })

    messages.success(request, "Review added successfully!")
    return redirect("reviews:movie_reviews", movie_id=movie.id)


# Edit review
@require_POST
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user_id = request.session.get("userid")

    if review.user_id != user_id:
        return JsonResponse({"success": False, "message": "Unauthorized."}, status=403)

    review.rating = request.POST.get("rating", review.rating)
    review.comment = request.POST.get("comment", review.comment)
    review.save()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        stars_html = "".join(
            f'<i class="bi bi-star{"-fill" if i < int(review.rating) else ""} text-warning"></i>'
            for i in range(5)
        )
        return JsonResponse({
            "success": True,
            "id": review.id,
            "comment": review.comment,
            "rating": review.rating,
            "stars_html": stars_html,
        })

    messages.success(request, "Review updated successfully!")
    return redirect("reviews:movie_reviews", movie_id=review.movie.id)


# Delete review
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user_id = request.session.get("userid")

    if review.user_id != user_id:
        return JsonResponse({"success": False, "message": "Unauthorized."}, status=403)

    review.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "id": review_id})

    messages.success(request, "Review deleted successfully!")
    return redirect("reviews:movie_reviews", movie_id=review.movie.id)
