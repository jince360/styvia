from django.db import models
from category.models import Category, MainCategory, SubCategory
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

PRODUCT_TYPE_CHOICES = [
    ("clothing", "Clothing"),
    ("footwear", "Footwear"),
    ("accessories", "Accessories"),
]

CLOTHING_SIZE_CHOICES = [
    ("xs", "Extra Small"),
    ("s", "Small"),
    ("m", "Medium"),
    ("l", "Large"),
    ("xl", "Extra Large"),
    ("xxl", "XXL"),
    ("xxxl", "XXXL"),
]

FOOTWEAR_SIZE_CHOICES = [
    ("uk3", "UK 3"),
    ("uk4", "UK 4"),
    ("uk5", "UK 5"),
    ("uk6", "UK 6"),
    ("uk7", "UK 7"),
    ("uk8", "UK 8"),
    ("uk9", "UK 9"),
    ("uk10", "UK 10"),
    ("uk11", "UK 11"),
    ("uk12", "UK 12"),
    ("uk13", "UK 13"),
]

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
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    description = models.TextField()
    product_type = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=20,default="clothing")
    
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
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.base_price

    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price<self.base_price
    
    def get_size_choice(self):
        if self.product_type == "clothing":
            return CLOTHING_SIZE_CHOICES
        elif self.product_type == "footwear":
            return FOOTWEAR_SIZE_CHOICES
        else:
            return []
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variants")
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=15, help_text="Size code (e.g., 'm', 'uk8')")
    size_display = models.CharField(max_length=100, blank=True, help_text="Measurement in inches/cm (e.g'Chest:38-40 inches' or 'Length: 27 inches')")

    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, help_text="Variant SKU")
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Price difference from base product (e.g., +50 for XL)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Product variant"
        verbose_name_plural = "Product Variants"
        ordering = ["color", "size"]
        unique_together = ["product", "color", "size"]
        indexes = [
            models.Index(fields=["product", "is_active"])
        ]

    def __str__(self):
        return f"{self.product.product_name} - {self.color} / {self.size}"
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def variant_price(self):
        return self.product.current_price +self.price_adjustment
    
    def get_size_display_full(self):
        choice = self.product.get_size_choice()
        size_label = self.size

        for i, j in choice:
            if i == self.size:
                size_label = j
                break

        if self.size_display:
            return f"{size_label} {self.size_display}"
        return size_label

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products/images", null=True,blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"
        ordering = ["-is_primary", "order"]

    def __str__(self):
        return f"{self.product.product_name} - images"



    

    

    

