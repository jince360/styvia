from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max, Q
import re
from .models import Product
from category.models import MainCategory, SubCategory, Category
from store.models import Brand
from design.models import MainCategoryBannerImage


def normalize_color_name(value):
    """Normalize color text for deduping/filtering (case, spaces, stray symbols)."""
    if not value:
        return ""

    cleaned = re.sub(r"[^a-zA-Z0-9\s/&,+-]", " ", str(value)).lower()
    parts = [
        re.sub(r"\s+", " ", part).strip(" -_")
        for part in re.split(r"\s*(?:and|&|/|,|\+)\s*", cleaned)
        if part and part.strip(" -_")
    ]

    if not parts:
        single = re.sub(r"\s+", " ", cleaned).strip(" -_")
        return single

    # Keep order while removing duplicates in multi-color names.
    seen = set()
    unique_parts = []
    for part in parts:
        if part not in seen:
            seen.add(part)
            unique_parts.append(part)

    return " and ".join(unique_parts)


def store(request, main_cat_slug=None):
    """Main category and all products view with filters"""
    main_cat = None
    main_cat_banner_slides = None

    products = Product.objects.filter(is_active=True)
    
    # Get filter parameters
    subcategory_slugs = request.GET.getlist('subcategory')
    category_slugs = request.GET.getlist('category')
    brand_ids = request.GET.getlist('brand')
    price_range = request.GET.get('price_range')
    colors = request.GET.getlist('color')
    discount = request.GET.get('discount')
    
    # Filter by main category
    if main_cat_slug:
        main_cat = get_object_or_404(MainCategory, slug=main_cat_slug, is_active=True)
        products = products.filter(product_main_category=main_cat)
        
        # Get banner slides
        main_cat_banner_slides = MainCategoryBannerImage.objects.filter(
            banner__main_category=main_cat,
            banner__is_active=True,
            is_active=True,
        ).select_related("banner__main_category").order_by("order")

    # Apply filters
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

    # Build filter data
    filter_data = {}
    
    if main_cat:
        # Get subcategories
        filter_data['subcategories'] = SubCategory.objects.filter(
            main_category=main_cat,
            is_active=True
        ).order_by('order', 'name')

        # Get categories (with dynamic filtering)
        categories_qs = Category.objects.filter(
            sub_category__main_category=main_cat,
            is_active=True
        )

        # Get brands (with dynamic filtering)
        brands_qs = Brand.objects.filter(
            products__product_main_category=main_cat,
            products__is_active=True,
            is_active=True
        )

        # Filter categories by selected subcategories
        if subcategory_slugs:
            categories_qs = categories_qs.filter(sub_category__slug__in=subcategory_slugs)
            brands_qs = brands_qs.filter(products__product_subcategory__slug__in=subcategory_slugs)

        # Filter brands by selected categories
        if category_slugs:
            brands_qs = brands_qs.filter(products__product_category__slug__in=category_slugs)

        filter_data['categories'] = categories_qs.select_related('sub_category').order_by('order', 'name')
        filter_data['brands'] = brands_qs.distinct().order_by('brand_name')
        
        # Get available colors
        filter_data['colors'] = Product.objects.filter(
            product_main_category=main_cat,
            is_active=True
        ).values_list('color', flat=True).distinct().order_by('color')
        
        # Get price range
        price_range_data = Product.objects.filter(
            product_main_category=main_cat,
            is_active=True
        ).aggregate(
            min_price=Min('base_price'),
            max_price=Max('base_price')
        )
        filter_data['price_range'] = price_range_data
    
    # Apply prefetch/select for optimization
    products = products.prefetch_related(
        "product_images",
        "variants"
    ).select_related(
        "brand",
        "seller",
        "product_main_category"
    )
    
    # Build selected filters for template
    selected_filters = {
        "subcategory_slugs": subcategory_slugs,
        "category_slugs": category_slugs,
        "brand_ids": brand_ids,
        "price_range": price_range,
        "colors": colors,
        "discount": discount,
    }
    
    return render(request, "store/store.html", {
        "products": products,
        "main_cat": main_cat,
        "main_cat_banner_slides": main_cat_banner_slides,
        "filter_data": filter_data,
        "selected_filters": selected_filters,
    })


def sub_category_store(request, main_cat_slug, sub_cat_slug):
    """Subcategory view with filters"""
    # Get main category and subcategory
    main_cat = get_object_or_404(MainCategory, slug=main_cat_slug, is_active=True)
    sub_cat = get_object_or_404(
        SubCategory, 
        slug=sub_cat_slug, 
        is_active=True, 
        main_category=main_cat
    )
    
    products = Product.objects.filter(
        is_active=True,
        product_subcategory=sub_cat
    )
    
    # Get filter parameters
    category_slugs = request.GET.getlist('category')
    brand_ids = request.GET.getlist('brand')
    selected_color_keys = [normalize_color_name(c) for c in request.GET.getlist('color')]
    selected_color_keys = [c for c in selected_color_keys if c]
    price_range = request.GET.get('price_range')
    discount = request.GET.get('discount')
    
    # Apply filters
    if category_slugs:
        products = products.filter(product_category__slug__in=category_slugs)
    
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)

    # Build raw->normalized color mapping for this subcategory scope.
    base_color_qs = Product.objects.filter(
        product_subcategory=sub_cat,
        is_active=True
    )
    if category_slugs:
        base_color_qs = base_color_qs.filter(product_category__slug__in=category_slugs)

    color_key_to_raw_values = {}
    for raw_color in base_color_qs.values_list("color", flat=True):
        color_key = normalize_color_name(raw_color)
        if not color_key:
            continue
        color_key_to_raw_values.setdefault(color_key, set()).add(raw_color)

    if selected_color_keys:
        raw_values_to_filter = set()
        for color_key in selected_color_keys:
            raw_values_to_filter.update(color_key_to_raw_values.get(color_key, set()))
        if raw_values_to_filter:
            products = products.filter(color__in=raw_values_to_filter)
    
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
    
    # Build filter data
    filter_data = {}
    
    # Get categories for this subcategory
    filter_data['categories'] = Category.objects.filter(
        sub_category=sub_cat,
        is_active=True
    ).order_by('order', 'name')
    
    # Get brands (with dynamic filtering)
    brands_qs = Brand.objects.filter(
        products__product_subcategory=sub_cat,
        products__is_active=True,
        is_active=True
    )
    
    # Filter brands by selected categories
    if category_slugs:
        brands_qs = brands_qs.filter(products__product_category__slug__in=category_slugs)
    
    filter_data['brands'] = brands_qs.distinct().order_by('brand_name')

    # Deduped, normalized colors for filter UI.
    filter_data['colors'] = sorted(color_key_to_raw_values.keys())
    
    # Apply prefetch/select for optimization
    products = products.prefetch_related(
        "product_images",
        "variants"
    ).select_related(
        "brand",
        "seller",
        "product_main_category",
        "product_subcategory"
    )
    
    # Build selected filters for template
    selected_filters = {
        "category_slugs": category_slugs,
        "brand_ids": brand_ids,
        "colors": selected_color_keys,
        "price_range": price_range,
        "discount": discount,
    }
    
    return render(request, "store/sub_cat_page.html", {
        "main_cat": main_cat,
        "sub_cat": sub_cat,
        "products": products,
        "filter_data": filter_data,
        "selected_filters": selected_filters,
    })
