from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "order", "created_at"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]

class MainCategoryBannerImageInline(admin.TabularInline):
    model = MainCategoryBannerImage
    extra = 1
    fields = ["image", "link", "order", "is_active"]


@admin.register(MainCategoryBanner)
class MainCategoryBannerAdmin(admin.ModelAdmin):
    list_display = ["main_category", "title", "order", "is_active"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active", "main_category"]
    search_fields = ["main_category__name", "title"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["main_category"]
    inlines = [MainCategoryBannerImageInline]
