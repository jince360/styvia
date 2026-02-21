from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import MainCategory
from design.models import MainCategoryBannerImage

# Create your views here.
def store(request, main_cat_slug=None):
    main_cat =None
    products=None
    main_cat_banner_slides = None
    
    if main_cat_slug !=None:
        main_cat = get_object_or_404(MainCategory, slug=main_cat_slug)
        products = Product.objects.filter(is_active=True, product_main_category=main_cat).prefetch_related("variants", "product_images").select_related("brand", "seller", "product_main_category")
        main_cat_banner_slides = MainCategoryBannerImage.objects.filter(
            banner__main_category=main_cat,
            banner__is_active=True,
            is_active=True,
        ).select_related("banner__main_category").order_by("order")

    else:

        products = Product.objects.filter(is_active=True).prefetch_related("variants", "product_images").select_related("brand", "seller", "product_main_category")

    return render(
        request,
        "store/store.html",
        {
            "products": products,
            "main_cat": main_cat,
            "main_cat_banner_slides": main_cat_banner_slides,
        },
    )
