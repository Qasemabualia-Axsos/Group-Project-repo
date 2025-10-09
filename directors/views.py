# directors/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST

from .models import Director
from .forms import DirectorForm

@require_http_methods(["GET"])
def director_list(request):
    qs = Director.objects.all()
    paginator = Paginator(qs, 12)  # 12 بطاقة في الصفحة
    page = request.GET.get("page")
    directors = paginator.get_page(page)
    return render(request, "directors/director_list.html", {"directors": directors})

@require_http_methods(["GET"])
def director_detail(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    return render(request, "directors/director_detail.html", {"director": director})

@require_http_methods(["GET", "POST"])
def director_create(request):
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            director = form.save()
            messages.success(request, f"تم إضافة {director.name} بنجاح.")
            return redirect("directors:director_detail", director_id=director.id)
        messages.error(request, "تحقق من الحقول، هناك أخطاء في الإدخال.")
    else:
        form = DirectorForm()
    return render(request, "directors/director_form.html", {"form": form, "title": "Add Director"})

@require_http_methods(["GET", "POST"])
def director_update(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث البيانات بنجاح.")
            return redirect("directors:director_detail", director_id=director.id)
        messages.error(request, "تحقق من الحقول، هناك أخطاء في الإدخال.")
    else:
        form = DirectorForm(instance=director)
    return render(request, "directors/director_form.html", {"form": form, "title": "Edit Director"})

@require_http_methods(["GET", "POST"])
def director_delete(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    if request.method == "POST":
        name = director.name
        director.delete()
        messages.success(request, f"تم حذف {name}.")
        return redirect("directors:director_list")
    return render(request, "directors/director_confirm_delete.html", {"director": director})

@require_http_methods(["GET"])
def director_api(request):
    directors = Director.objects.all().values(
        "id", "name", "slug", "nationality", "imdb_url", "website", "is_active"
    )
    return JsonResponse(list(directors), safe=False)
