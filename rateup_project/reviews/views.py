from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # prevent duplicate reviews by the same user
    if Review.objects.filter(movie=movie, user=request.user).exists():
        return redirect("movies:movie_detail", pk=movie.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect("movies:movie_detail", pk=movie.id)
    else:
        form = ReviewForm()

    return render(request, "reviews/review_form.html", {"form": form, "movie": movie})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("movies:movie_detail", pk=review.movie.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_form.html", {"form": form, "movie": review.movie})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie_id = review.movie.id

    if request.method == "POST":  # confirm delete with a form
        review.delete()
        return redirect("movies:movie_detail", pk=movie_id)

    return render(request, "reviews/review_confirm_delete.html", {"review": review})
