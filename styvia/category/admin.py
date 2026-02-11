from django.contrib import admin
from .models import *
# Register your models here.

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ["name","order", "is_active", ]
    

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fields = ["name","order", "is_active"]
    

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "created_at", "is_active"]
    list_editable = ["order", "is_active"]
    list_filter = ["name", "is_active", "order", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug":("name",),}
    readonly_fields = ["created_at", "updated_at"]

    inlines = [SubCategoryInline]

    fieldsets = (
        ("Basic Information", {
            "fields":("name", "slug", "order")
        }),
        ("Media", {
            "fields":("main_category_image",)
        }),
        ("Status", {
            "fields":("is_active", "created_at", "updated_at")
        })
    )

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "main_category", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    list_filter =["is_active", "main_category", "created_at"]
    search_fields = ["name", "main_category__name"]
    prepopulated_fields = {"slug":("name",),}
    readonly_fields = ["created_at", "updated_at"]

    inlines = [CategoryInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("main_category","name", "slug", "order"),
        }),
        ("Media", {
            "fields": ("sub_category_image",),
        }),
        ("Status", {
            "fields": ("is_active", "created_at", "updated_at"),
        }),
    )
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "sub_category", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active", "sub_category__main_category", "sub_category", "created_at"]
    search_fields = ["name", "sub_category__name", "description"]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ("Basic Information", {
            "fields": ("sub_category", "name", "slug", "description", "order"),
        }),
        ("Media", {
            "fields": ("cat_image",),
        }),
        ("Status", {
            "fields": ("is_active", "created_at", "updated_at"),
        }),
    )
    