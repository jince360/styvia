from django.shortcuts import render
from category.models import *
from design.models import *
# Create your views here.
def home(request):
    hero_images = Hero.objects.filter(is_active=True).order_by("created_at")
    return render(request, "core/html/home.html", {"hero_images":hero_images})