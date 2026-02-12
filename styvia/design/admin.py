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
