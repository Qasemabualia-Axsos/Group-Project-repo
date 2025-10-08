from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Review
from movies.models import Movies
from accounts.models import Users
from django.http import JsonResponse
from django.template.loader import render_to_string




def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    reviews = Review.objects.filter(movie=movie).select_related("user")

    # Handle AJAX operations (add, update, delete)
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        action = request.POST.get("action")
        review_id = request.POST.get("review_id")
        comment = request.POST.get("comment")
        rating = request.POST.get("rating")

        user_id = request.session.get("userid")
        if not user_id:
            return JsonResponse({"success": False, "message": "You must be logged in."})

        if action == "add":
            Review.objects.create(movie=movie, user_id=user_id, comment=comment, rating=rating)
            message = "Review added successfully!"

        elif action == "update" and review_id:
            review = Review.objects.filter(id=review_id, user_id=user_id).first()
            if review:
                review.comment = comment
                review.rating = rating
                review.save()
                message = "Review updated successfully!"
            else:
                return JsonResponse({"success": False, "message": "Review not found or unauthorized."})

        elif action == "delete" and review_id:
            Review.objects.filter(id=review_id, user_id=user_id).delete()
            message = "Review deleted successfully!"

        # Re-render reviews section with full context (important fix)
        reviews = Review.objects.filter(movie=movie).select_related("user")
        html = render(request, "reviews/reviews_list.html", {
            "reviews": reviews,
            "request": request,  # ✅ This keeps session data in template
        }).content.decode("utf-8")

        return JsonResponse({"success": True, "html": html, "message": message})

    return render(request, "reviews/movie_reviews.html", {
        "movie": movie,
        "reviews": reviews,
    })






