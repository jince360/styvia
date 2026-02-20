from django.db import models
from category.models import Category, MainCategory, SubCategory
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
from sizemanager.models import Size, SizeGroup
# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    brand_logo = models.ImageField(upload_to="brands", blank=True, null=True)
    brand_images = models.ImageField(upload_to="brand_images", blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["brand_name"]
        indexes = [
            models.Index(fields=["is_active", "is_popular"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_name
    

class Seller(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_profile")
    business_name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    business_phone = models.CharField(max_length=15)
    business_email = models.EmailField(max_length=254,unique=True)
    license = models.CharField(max_length=50, unique=True)

    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    postal_code = models.CharField(max_length=10)

    is_verified = models.BooleanField(default=False, help_text="Admin must verify seller")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
        ordering = ["business_name"]
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.business_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name
    


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="products")
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, related_name="products")
    product_main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, related_name="products")
    product_subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name="products")
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")

    product_name = models.CharField(max_length=200)
    product_detailed_name = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, editable=False, help_text="Auto-generated Stock Keeping Unit")
    description = models.TextField()
    product_type = models.CharField(choices=[
            ("topwear", "Topwear"),
            ("bottomwear", "Bottomwear"),
            ("footwear", "Footwear"),
            ("accessories", "Accessories"),

    ], max_length=20,default="topwear")

    size_group = models.ForeignKey(SizeGroup, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    view_count = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_on"]
        indexes = [
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["product_type"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        if not self.sku:
            main_cat = self.product_main_category.name[:3].upper() if self.product_main_category else "XXX"
            cat = self.product_category.name[:3].upper() if self.product_category else "XXX"
            random_part = uuid.uuid4().hex[:4].upper()
            color_code = self.color[:3].upper()
            self.sku = f"{main_cat}-{cat}-{color_code}-{random_part}"
        super().save(*args, **kwargs)

    

    def __str__(self):
        return self.product_name
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.base_price
    
    @property
    def get_primary_image(self):
        image = self.product_images.filter(is_primary=True).first()
        if not image:
            image = self.product_images.first()
        return image



    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price<self.base_price
    
    def get_available_sizes(self):
        if self.size_group:
            return self.size_group.sizes.filter(is_active=True)
        return Size.objects.none()

    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variants")
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True,related_name="variants")
    size_display = models.CharField(max_length=100, blank=True, help_text="Measurement in inches/cm (e.g'Chest:38-40 inches' or 'Length: 27 inches')")

    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True, editable=False, help_text="Variant SKU")
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Price difference from base product (e.g., +50 for XL)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Product variant"
        verbose_name_plural = "Product Variants"
        ordering = ["size__order"]
        unique_together = ["product", "size"]
        indexes = [
            models.Index(fields=["product", "is_active"])
        ]

        
    def save(self, *args, **kwargs):
        if not self.sku:
            random_part = uuid.uuid4().hex[:4].upper()
            size_code = self.size.name.upper() if self.size else "NA"
            self.sku = f"{self.product.sku}-{size_code}-{random_part}"
        self.full_clean()
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.product.product_name} - {self.size}"
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def variant_price(self):
        return self.product.current_price +self.price_adjustment
    
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products/images")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.product.product_images.filter(is_primary=True).exists():
            self.is_primary =True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"
        ordering = ["-is_primary", "order"]

    def __str__(self):
        return f"{self.product.product_name} - images"



    

    

    

