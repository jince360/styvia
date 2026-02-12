from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Hero(models.Model):
    title = models.CharField(max_length=50, help_text="Hero banner title")
    desktop_image = models.ImageField(upload_to="hero_images/desktop", help_text="Recommended size: 1920x800px")
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

