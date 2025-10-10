from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Director
from .forms import DirectorForm

# List all directors with search + pagination
def director_list(request):
    q = (request.GET.get("q") or "").strip()
    qs = Director.objects.all().order_by("name")
    if q:
        qs = qs.filter(name__icontains=q)
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "directors/director_list.html", {"page_obj": page_obj, "q": q})

# Director details
def director_detail(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    return render(request, "directors/director_detail.html", {"director": director})

# Create new director
def director_create(request):
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            director = form.save()
            return redirect("directors:director_detail", director_id=director.id)
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
    directors = Director.objects.all().values("id", "name", "bio", "profile_img")
    return JsonResponse(list(directors), safe=False)
