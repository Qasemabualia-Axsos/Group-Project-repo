from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Actor
from .forms import ActorForm

# List all actors with search + pagination
def actor_list(request):
    q = (request.GET.get("q") or "").strip()
    qs = Actor.objects.all().order_by("name")
    if q:
        qs = qs.filter(name__icontains=q)
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "actors/actor_list.html", {"page_obj": page_obj, "q": q})

# Actor detail
def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    return render(request, "actors/actor_detail.html", {"actor": actor})

# Create actor
def actor_create(request):
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            actor = form.save()
            return redirect("actors:actor_detail", actor_id=actor.id)
    else:
        form = ActorForm()
    return render(request, "actors/actor_form.html", {"form": form, "title": "Add Actor"})

# Update actor
def actor_update(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES, instance=actor)
        if form.is_valid():
            form.save()
            return redirect("actors:actor_detail", actor_id=actor.id)
    else:
        form = ActorForm(instance=actor)
    return render(request, "actors/actor_form.html", {"form": form, "title": "Edit Actor"})

# Delete actor
def actor_delete(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    if request.method == "POST":
        actor.delete()
        return redirect("actors:actor_list")
    return render(request, "actors/actor_confirm_delete.html", {"actor": actor})

# API endpoint for AJAX
def actor_api(request):
    actors = Actor.objects.all().values("id", "name", "bio", "profile_img")
    return JsonResponse(list(actors), safe=False)

