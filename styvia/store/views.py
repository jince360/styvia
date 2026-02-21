from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max, Q
from .models import Product
from category.models import MainCategory, SubCategory, Category
from store.models import Brand
from design.models import MainCategoryBannerImage


def store(request, main_cat_slug=None):
    main_cat = None
    main_cat_banner_slides = None

    products = Product.objects.filter(is_active=True)
    
    # ✅ Changed to getlist() for multiple selections
    subcategory_slugs = request.GET.getlist('subcategory')
    category_slugs = request.GET.getlist('category')
    brand_ids = request.GET.getlist('brand')
    price_range = request.GET.get('price_range')
    colors = request.GET.getlist('color')
    
    if main_cat_slug:
        main_cat = get_object_or_404(MainCategory, slug=main_cat_slug, is_active=True)
        products = products.filter(product_main_category=main_cat)
        
        main_cat_banner_slides = MainCategoryBannerImage.objects.filter(
            banner__main_category=main_cat,
            banner__is_active=True,
            is_active=True,
        ).select_related("banner__main_category").order_by("order")
    
    # ✅ Changed to __in for multiple selections
    if subcategory_slugs:
        products = products.filter(product_subcategory__slug__in=subcategory_slugs)
    
    if category_slugs:
        products = products.filter(product_category__slug__in=category_slugs)
    
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)
    
    if price_range:
        try:
            min_price, max_price = price_range.split('-')
            min_price = int(min_price)
            max_price = int(max_price)
            
            products = products.filter(
                Q(sale_price__gte=min_price, sale_price__lte=max_price) |
                Q(sale_price__isnull=True, base_price__gte=min_price, base_price__lte=max_price)
            )
        except ValueError:
            pass
    
    if colors:
        products = products.filter(color__in=colors)

    filter_data = {}
    
    if main_cat:
        filter_data['subcategories'] = SubCategory.objects.filter(
            main_category=main_cat,
            is_active=True
        ).order_by('order', 'name')
        
        filter_data['categories'] = Category.objects.filter(
            sub_category__main_category=main_cat,
            is_active=True
        ).select_related('sub_category').order_by('order', 'name')
        
        filter_data['brands'] = Brand.objects.filter(
            products__product_main_category=main_cat,
            products__is_active=True,
            is_active=True
        ).distinct().order_by('brand_name')
        
        filter_data['colors'] = Product.objects.filter(
            product_main_category=main_cat,
            is_active=True
        ).values_list('color', flat=True).distinct().order_by('color')
        
        price_range_data = Product.objects.filter(
            product_main_category=main_cat,
            is_active=True
        ).aggregate(
            min_price=Min('base_price'),
            max_price=Max('base_price')
        )
        filter_data['price_range'] = price_range_data
    
    products = products.prefetch_related(
        "product_images",
        "variants"
    ).select_related(
        "brand",
        "seller",
        "product_main_category"
    )
    
    return render(request, "store/store.html", {
        "products": products,
        "main_cat": main_cat,
        "main_cat_banner_slides": main_cat_banner_slides,
        "filter_data": filter_data,
    })