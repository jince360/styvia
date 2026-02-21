from django.db import models
from django.core.exceptions import ValidationError
from category.models import MainCategory
# Create your models here.
class Hero(models.Model):
    title = models.CharField(max_length=50, help_text="Hero banner title")
    desktop_image = models.ImageField(upload_to="hero_images/desktop", help_text="Recommended size: 1920x540px")
    mobile_image = models.ImageField(upload_to="hero_images/mobile", help_text="Recommended size: 768x600px")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    link = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero banner"
        verbose_name_plural = "Hero banners"
        ordering = ["order","-created_at"]
        indexes = [
            models.Index(fields=["is_active", "order"])
        ]
        
    def __str__(self):
        return f"{self.title}"
    
    def clean(self):
        if self.is_active:
            active_count = Hero.objects.filter(is_active=True).exclude(pk=self.pk).count()
            if active_count >= 6:
                raise ValidationError("Maximum 6 hero images are allowed. Please deactivate one first")


class MainCategoryBanner(models.Model):

    main_category = models.OneToOneField(MainCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Main category banner"
        verbose_name_plural = "Main category banners"
        ordering = ["order", "main_category__name"]
    def __str__(self):
        return self.title if self.title else "banner image"
    

class MainCategoryBannerImage(models.Model):
    banner = models.ForeignKey(MainCategoryBanner, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="banner_images", help_text="Recommended size: 1920x540px")
    link = models.URLField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Main category banner image"
        verbose_name_plural = "Main category banner images"
        ordering = ["order", "-created_at"]
        indexes = [
            models.Index(fields=["banner", "is_active", "order"])
        ]

    def clean(self):
        if self.is_active and self.banner_id:
            active_count = MainCategoryBannerImage.objects.filter(banner=self.banner, is_active=True).exclude(pk=self.pk).count()
            if active_count >= 6:
                raise ValidationError("Maximum 6 hero images are allowed. Please deactivate one first")

    def __str__(self):
        return f"{self.banner.main_category.name} - images"
    

    