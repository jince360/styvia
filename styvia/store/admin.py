from django.contrib import admin
from .models import Brand,Seller,ProductVariant,ProductImage,Product
# Register your models here.

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["brand_name", "is_active", "is_popular", "created_at"]
    list_editable = ["is_active", "is_popular"]
    list_filter = ["is_active", "is_popular", "created_at"]
    search_fields = ["brand_name"]
    prepopulated_fields = {"slug":("brand_name",)}
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("basic Information", {
            "fields": ("brand_name", "slug"),
        }),
        ("Media", {
            "fields": ("brand_logo", "brand_images"),
        }),
        ("Status", {
            "fields": ("is_active", "is_popular", "created_at", "updated_at"),
        }),
    )
    
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["business_name", "user", "is_verified", "is_active", "created_at"]
    list_editable = ["is_verified", "is_active"]
    list_filter = ["is_verified", "is_active", "country", "state", "created_at"]
    search_fields = ["business_name", "user__email", "business_email", "license"]
    readonly_fields = ["slug", "created_at", "updated_at"]
    actions = ["verify_seller", "unverify_seller"]

    fieldsets = (
        ("User Account", {
            "fields": ("user",),
        }),
    
        ("Business Information", {
            "fields": ("business_name", "slug", "license")
        }),
        ("Contact", {
            "fields": ("business_phone", "business_email")
        }),
        ("Address", {
            "fields": ("address_line1", "address_line2", "city", "state", "country", "postal_code")
        }),
        ("Status", {
            "fields": ("is_verified", "is_active", "created_at", "updated_at")
        })
    )

    def verify_seller(self, request, queryset):
        queryset.update(is_verified=True)
    verify_seller.short_description = "Verify selected seller"

    def unverify_seller(self,request, queryset):
        queryset.update(is_verified=False)
    unverify_seller.short_description = "Unverify selected seller"

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ["color", "size", "size_display", "stock", "sku", "price_adjustment", "is_active"]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "is_primary", "order"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name", "product_type", "brand", "seller","base_price", "sale_price","is_active", "is_featured","view_count","created_on"]
    list_editable = ["is_active", "is_featured"]
    list_filter = ["product_type", "is_active", "is_featured", "brand","product_main_category","created_on"]
    search_fields = ["product_name", "sku", "description", "brand__brand_name"]
    prepopulated_fields = {"slug": ("product_name",)}
    readonly_fields = ["view_count", "created_on", "updated_on"]
    autocomplete_fields = ["brand", "seller", "product_main_category", "product_subcategory", "product_category"]

    inlines = [ProductVariantInline, ProductImageInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("product_name", "slug", "sku", "product_type", "description")
        }),
        ("Categories", {
            "fields": ("product_main_category", "product_subcategory", "product_category")
        }),
        ("Relationships", {
            "fields": ("brand", "seller")
        }),
        ("Pricing", {
            "fields": ("base_price", "sale_price")
        }),
        ("Status & Metrics", {
            "fields": ("is_active", "is_featured", "view_count", "created_on", "updated_on")
        })
    )

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["product", "color", "size", "stock", "sku", "is_active", "created_at"]
    list_editable = ["stock", "is_active"]
    list_filter = ["is_active", "color", "size", "product__product_type"]
    search_fields = ["product__product_name", "sku", "color"]
    readonly_fields = ["created_at", "updated_at"]
    
    fieldsets = (
        ("Product", {
            "fields": ("product",)
        }),
        ("Variant Details", {
            "fields": ("color", "size", "size_display", "sku")
        }),
        ("Inventory & Pricing", {
            "fields": ("stock", "price_adjustment")
        }),
        ("Status", {
            "fields": ("is_active", "created_at", "updated_at")
        })
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "is_primary", "order", "created_at"]
    list_editable = ["is_primary", "order"]
    list_filter = ["is_primary", "created_at"]
    search_fields = ["product__product_name", "alt_text"]
    readonly_fields = ["created_at"]
    
    fieldsets = (
        ("Product", {
            "fields": ("product",)
        }),
        ("Image", {
            "fields": ("image", "alt_text")
        }),
        ("Display", {
            "fields": ("is_primary", "order", "created_at")
        })
    )



    