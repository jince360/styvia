from django.db import models

# Create your models here.
class SizeGroup(models.Model):

    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Group size"
        verbose_name_plural = "Group sizes"
    
    def __str__(self):
        return self.name
 

class Size(models.Model):
   
    group = models.ForeignKey(SizeGroup,on_delete=models.CASCADE,related_name="sizes")
    name = models.CharField(max_length=20)
    order = models.PositiveIntegerField(default=0,help_text="Display order (lower number = shown first)")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ["order", "name"]
        unique_together = ["group", "name"]

    def __str__(self):
        return f"{self.group.name} - {self.name}"