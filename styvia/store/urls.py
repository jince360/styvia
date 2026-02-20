from django.urls import path
from .views import *

urlpatterns = [
    path("", store, name="store"),
    path("<slug:main_cat_slug>/", store, name="products_by_main_cat")
]
