from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Director
from .forms import DirectorForm

# List all directors
def director_list(request):
    directors = Director.objects.all()
    return render(request, "directors/director_list.html", {"directors": directors})

# Director details
def director_detail(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    return render(request, "directors/director_detail.html", {"director": director})

# Create new director
def director_create(request):
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("directors:director_list")
    else:
        form = DirectorForm()
    return render(request, "directors/director_form.html", {"form": form, "title": "Add Director"})

# Update director
def director_update(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            return redirect("directors:director_detail", director_id=director.id)
    else:
        form = DirectorForm(instance=director)
    return render(request, "directors/director_form.html", {"form": form, "title": "Edit Director"})

# Delete director
def director_delete(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    if request.method == "POST":
        director.delete()
        return redirect("directors:director_list")
    return render(request, "directors/director_confirm_delete.html", {"director": director})

# API (AJAX/JSON)
def director_api(request):
    directors = Director.objects.all().values("id", "name", "bio")
    return JsonResponse(list(directors), safe=False)
