from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Director
from .forms import DirectorForm

def director_list(request):
    directors = Director.objects.all()
    return render(request, "directors/director_list.html", {"directors": directors})

def director_detail(request, pk):
    director = get_object_or_404(Director, pk=pk)
    return render(request, "directors/director_detail.html", {"director": director})

@login_required
def director_create(request):
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("directors:director_list")
    else:
        form = DirectorForm()
    return render(request, "directors/director_form.html", {"form": form})

@login_required
def director_update(request, pk):
    director = get_object_or_404(Director, pk=pk)
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            return redirect("directors:director_detail", pk=pk)
    else:
        form = DirectorForm(instance=director)
    return render(request, "directors/director_form.html", {"form": form})

@login_required
def director_delete(request, pk):
    director = get_object_or_404(Director, pk=pk)
    director.delete()
    return redirect("directors:director_list")
