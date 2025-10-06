from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category
from .form import CategoryForm

# API
from rest_framework import generics
from .serializers import CategorySerializer

# ---------- HTML Views ----------
class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "categories/index.html", {"categories": categories})

class CategoryDetailView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, "categories/detail.html", {"category": category})

class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, "categories/form.html", {"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories:index")
        return render(request, "categories/form.html", {"form": form})

class CategoryUpdateView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, "categories/form.html", {"form": form})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories:index")
        return render(request, "categories/form.html", {"form": form})

class CategoryDeleteView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect("categories:index")

# ---------- API Views ----------
class CategoryListAPI(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
