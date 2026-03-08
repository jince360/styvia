from django.urls import path
from .views import *

urlpatterns = [
    path("", store, name="store"),
    path("<slug:main_cat_slug>/", store, name="products_by_main_cat"),
    path("<slug:main_cat_slug>/<slug:sub_cat_slug>/",sub_category_store,name="product_by_sub_cat"),
]
