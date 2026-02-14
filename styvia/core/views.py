from django.shortcuts import render
from store.models import Brand
from design.models import Hero
# Create your views here.
def home(request):
    hero_images = Hero.objects.filter(is_active=True).order_by("-created_at")
    brands = Brand.objects.filter(is_active=True, is_popular=True)
    return render(request, "core/html/home.html", {"hero_images":hero_images, "brands":brands})