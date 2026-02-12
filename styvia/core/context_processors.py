from category.models import MainCategory

def category_processor(request):
    main_category = MainCategory.objects.filter(is_active=True).prefetch_related("subcategories__categories").order_by("order")
    return {"main_categories":main_category}