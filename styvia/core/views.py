from django.shortcuts import render
from category.models import *
# Create your views here.
def home(request):
    main_categories = MainCategory.objects.filter(is_active=True)
    return render(request, "core/html/home.html", {"main_categories":main_categories})