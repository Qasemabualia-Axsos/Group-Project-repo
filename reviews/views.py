from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Review
from movies.models import Movies
from accounts.models import Users


# # 1️⃣ List all reviews for a specific movie
# def movie_reviews(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
#     reviews = movie.reviews.all().select_related('user')
#     return render(request, 'reviews/movie_reviews.html', {'movie': movie, 'reviews': reviews})


# # 2️⃣ Add a new review
# def add_review(request, movie_id):
#     if 'userid' not in request.session:  # ✅ fixed key name
#         messages.error(request, 'You must log in to add a review.')
#         return redirect('accounts:login_page')

#     movie = get_object_or_404(Movie, id=movie_id)
#     user = User.objects.get(id=request.session['userid'])  # ✅ fixed key name

#     if request.method == 'POST':
#         rating = request.POST.get('rating')
#         comment = request.POST.get('comment', '')

#         if not rating or int(rating) < 1 or int(rating) > 5:
#             messages.error(request, 'Rating must be between 1 and 5.')
#             return redirect('reviews:add_review', movie_id=movie.id)

#         Review.objects.create(
#             user=user,
#             movie=movie,
#             rating=int(rating),
#             comment=comment
#         )

#         messages.success(request, 'Your review has been added successfully!')
#         return redirect('reviews:movie_reviews', movie_id=movie.id)

#     return render(request, 'reviews/add_review.html', {'movie': movie})


# # 3️⃣ Edit a review
# def edit_review(request, review_id):
#     if 'userid' not in request.session:
#         messages.error(request, 'You must log in first.')
#         return redirect('accounts:login_page')

#     review = get_object_or_404(Review, id=review_id, user__id=request.session['userid'])

#     if request.method == 'POST':
#         review.rating = request.POST.get('rating')
#         review.comment = request.POST.get('comment', '')
#         review.save()
#         messages.success(request, 'Your review has been updated!')
#         return redirect('reviews:movie_reviews', movie_id=review.movie.id)

#     return render(request, 'reviews/edit_review.html', {'review': review})


# # 4️⃣ Delete a review
# def delete_review(request, review_id):
#     if 'userid' not in request.session:
#         messages.error(request, 'You must log in first.')
#         return redirect('accounts:login_page')

#     review = get_object_or_404(Review, id=review_id, user__id=request.session['userid'])
#     movie_id = review.movie.id
#     review.delete()
#     messages.success(request, 'Your review has been deleted.')
#     return redirect('reviews:movie_reviews', movie_id=movie_id)




def movie_reviews(request, movie_id):
    # Get movie and all its reviews
    movie = get_object_or_404(Movies, id=movie_id)
    reviews = movie.reviews.all().select_related('user')

    if 'userid' not in request.session:
        user = None
    else:
        user = Users.objects.get(id=request.session['userid'])

    # --------------------
    # Handle Delete
    # --------------------
    delete_id = request.GET.get('delete')
    if delete_id and user:
        review_to_delete = get_object_or_404(Review, id=delete_id, user=user)
        review_to_delete.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('reviews:movie_reviews', movie_id=movie.id)

    # --------------------
    # Handle Edit GET
    # --------------------
    edit_id = request.GET.get('edit')
    edit_review = None
    if edit_id and user:
        edit_review = get_object_or_404(Review, id=edit_id, user=user)

    # --------------------
    # Handle POST for Add/Edit
    # --------------------
    if request.method == 'POST' and user:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        review_id = request.POST.get('review_id')

        # Validate rating
        if not rating or int(rating) < 1 or int(rating) > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
            return redirect('reviews:movie_reviews', movie_id=movie.id)

        if review_id:  # Edit existing review
            review = get_object_or_404(Review, id=review_id, user=user)
            review.rating = int(rating)
            review.comment = comment
            review.save()
            messages.success(request, 'Your review has been updated!')
        else:  # Add new review
            Review.objects.create(user=user, movie=movie, rating=int(rating), comment=comment)
            messages.success(request, 'Your review has been added successfully!')

        return redirect('reviews:movie_reviews', movie_id=movie.id)

    # --------------------
    # Render template
    # --------------------
    return render(request, 'reviews/movie_reviews.html', {
        'movie': movie,
        'reviews': reviews,
        'edit_review': edit_review,
        'edit_review_id': edit_review.id if edit_review else None,
    })