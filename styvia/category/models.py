from django.db import models
from django.utils.text import slugify

# Create your models here.

class MainCategory(models.Model):

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    order = models.PositiveIntegerField(default=0, help_text="Display order in navbar")
    main_category_image = models.ImageField(upload_to="categories/main/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Main category"
        verbose_name_plural = "Main categories"
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["is_active", "order"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):

    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name="subcategories")
    name= models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order in navbar")
    sub_category_image = models.ImageField(upload_to="categories/sub/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sub category"
        verbose_name_plural = "Sub categories"
        ordering = ["order", "name"]
        unique_together = ["main_category", "slug"]
        indexes = [
            models.Index(fields=["main_category", "is_active", "order"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.main_category.name} - {self.name}"
    
class Category(models.Model):

    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order in navbar")
    cat_image = models.ImageField(upload_to="categories/category", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]
        unique_together = ["sub_category", "slug"]
        indexes = [
            models.Index(fields=["sub_category", "is_active", "order"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sub_category.name} - {self.name}"
    




