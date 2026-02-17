from django.contrib import admin
from .models import Size, SizeGroup
# Register your models here.

class SizeInline(admin.TabularInline):
    model = Size
    extra = 1
    fields = ["name", "order", "is_active"]

@admin.register(SizeGroup)
class SizeGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_editable = ["is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    inlines = [SizeInline]

    fieldsets = (
        ("Size Group", {
            "fields": ("name", "is_active")}),
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "order", "is_active"]
    list_editable = ["is_active", "order"]
    search_fields = ["name", "group__name"]
    list_filter = ["group", "is_active"]
    autocomplete_fields = ["group"]
