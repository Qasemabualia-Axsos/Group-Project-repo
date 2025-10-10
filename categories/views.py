from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.conf import settings
from accounts.models import Users
from .models import Category


# -------------------------------
# Helpers
# -------------------------------
def _is_logged_in(request):
    return 'userid' in request.session


def _current_user(request):
    """Return current logged in user from session."""
    if not _is_logged_in(request):
        return None
    try:
        return Users.objects.get(id=request.session['userid'])
    except Users.DoesNotExist:
        return None


def _require_admin(request):
    """Check if current user is staff/superuser."""
    user = _current_user(request)
    return (
        user is not None
        and getattr(user, "is_authenticated", False)
        and (getattr(user, "is_staff", False) or getattr(user, "is_superuser", False))
    )


# -------------------------------
# Views
# -------------------------------
def categories_page(request):
    """Render categories page with admin flag for template."""
    is_admin = _require_admin(request)
    categories = Category.objects.all()
    return render(request, "categories/index.html", {
        "is_admin": is_admin,
        "categories": categories
    })


@require_http_methods(["GET"])
def api_list(request):
    """Return all categories as JSON."""
    qs = Category.objects.all()
    data = [{
        "id": c.id,
        "name": c.name,
        "description": c.description or "",
        "image": request.build_absolute_uri(c.image.url) if c.image else "",
    } for c in qs]
    return JsonResponse({"categories": data}, status=200)


@require_http_methods(["POST"])
def api_create(request):
    """Create a category (admin only)."""
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
            "id": cat.id,
            "name": cat.name,
            "description": cat.description or "",
            "image": request.build_absolute_uri(cat.image.url) if cat.image else ""
        }
    }, status=201)


@require_http_methods(["POST"])
def api_update(request, pk):
    """Update a category (admin only)."""
    if not _require_admin(request):
        return HttpResponseForbidden("Only admin can update.")

    cat = get_object_or_404(Category, pk=pk)
    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()
    image = request.FILES.get("image")

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
            "id": cat.id,
            "name": cat.name,
            "description": cat.description or "",
            "image": request.build_absolute_uri(cat.image.url) if cat.image else ""
        }
    }, status=200)


@require_http_methods(["POST"])
def api_delete(request, pk):
    """Delete a category (admin only)."""
    if not _require_admin(request):
        return HttpResponseForbidden("Only admin can delete.")

    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    return JsonResponse({"status": "success"}, status=200)


def create_category(request):
    """Extra category creation with validation (admin only)."""
    if request.method == "POST":
        if not _require_admin(request):
            return HttpResponseForbidden("Only admin can create.")

        errors = Category.objects.category_validator(request.POST)
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        Category.objects.create(
            name=request.POST.get("name").strip(),
            description=request.POST.get("description").strip(),
            image=request.FILES.get("image")
        )
        return JsonResponse({"status": "success"})
