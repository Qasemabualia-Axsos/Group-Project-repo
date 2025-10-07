from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
from accounts.models import Users
from .models import Category

def _is_logged_in(request):
    return 'userid' in request.session

def _current_user(request):
    if not _is_logged_in(request):
        return None
    try:
        return Users.objects.get(id=request.session['userid'])
    except Users.DoesNotExist:
        return None

def _require_admin(request):
    user = _current_user(request)
    return (user is not None) and user.is_admin

def categories_page(request):
    is_admin = _require_admin(request)
    return render(request, 'categories/index.html', {'is_admin': is_admin})

@require_http_methods(["GET"])
def api_list(request):
    qs = Category.objects.all()
    data = [{
        "id": c.id,
        "name": c.name,
        "description": c.description or "",
        "image": (request.build_absolute_uri(c.image.url) if c.image else ""),
    } for c in qs]
    return JsonResponse({"categories": data}, status=200)

@require_http_methods(["POST"])
def api_create(request):
    if not _require_admin(request):
        return HttpResponseForbidden("Only admin can create.")

    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()
    image = request.FILES.get("image")

    errors = {}
    if not name:
        errors["name"] = "Name is required"
    elif Category.objects.filter(name__iexact=name).exists():
        errors["name"] = "Category name already exists"

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    cat = Category.objects.create(name=name, description=description, image=image)
    return JsonResponse({
        "status": "success",
        "category": {
            "id": cat.id, "name": cat.name, "description": cat.description or "",
            "image": (request.build_absolute_uri(cat.image.url) if cat.image else "")
        }
    }, status=201)

@require_http_methods(["POST"])
def api_update(request, pk):
    if not _require_admin(request):
        return HttpResponseForbidden("Only admin can update.")

    cat = get_object_or_404(Category, pk=pk)
    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()
    image = request.FILES.get("image", None)

    errors = {}
    if not name:
        errors["name"] = "Name is required"
    elif Category.objects.filter(name__iexact=name).exclude(pk=pk).exists():
        errors["name"] = "Category name already exists"

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    cat.name = name
    cat.description = description
    if image:
        cat.image = image
    cat.save()

    return JsonResponse({
        "status": "success",
        "category": {
            "id": cat.id, "name": cat.name, "description": cat.description or "",
            "image": (request.build_absolute_uri(cat.image.url) if cat.image else "")
        }
    }, status=200)

@require_http_methods(["POST"])
def api_delete(request, pk):
    if not _require_admin(request):
        return HttpResponseForbidden("Only admin can delete.")

    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    return JsonResponse({"status": "success"}, status=200)



def create_category(request):
    if request.method == "POST":
        errors = Category.objects.category_validator(request.POST)
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        Category.objects.create(
            name=request.POST.get("name").strip(),
            description=request.POST.get("description").strip(),
            image=request.FILES.get("image")
        )
        return JsonResponse({"status": "success"})
