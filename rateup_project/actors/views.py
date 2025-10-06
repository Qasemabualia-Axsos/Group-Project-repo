from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Actor
from .forms import ActorForm

def actor_list(request):
    actors = Actor.objects.all()
    return render(request, "actors/actor_list.html", {"actors": actors})

def actor_detail(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    return render(request, "actors/actor_detail.html", {"actor": actor})

@login_required
def actor_create(request):
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("actors:actor_list")
    else:
        form = ActorForm()
    return render(request, "actors/actor_form.html", {"form": form})

@login_required
def actor_update(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES, instance=actor)
        if form.is_valid():
            form.save()
            return redirect("actors:actor_detail", pk=pk)
    else:
        form = ActorForm(instance=actor)
    return render(request, "actors/actor_form.html", {"form": form})

@login_required
def actor_delete(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    actor.delete()
    return redirect("actors:actor_list")
