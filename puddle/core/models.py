from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class UploadedImage(models.Model):  
    image = models.ImageField(upload_to='item_images')  
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):  
        return f"Image uploaded at {self.uploaded_at}"  

class ExcelData(models.Model):
    name = models.CharField(max_length=100)
    marks = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Marks cannot be negative"),
            MaxValueValidator(100, message="Marks cannot exceed 100")
        ]
    )
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Excel Data'
        verbose_name_plural = 'Excel Data'

    def __str__(self):
        return f"{self.name} - {self.marks}"

    def clean(self):
        if self.marks < 0 or self.marks > 100:
            raise ValidationError("Marks must be between 0 and 100")

# Create your models here.
