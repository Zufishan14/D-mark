from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator  




class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Item(models.Model):
        category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
        name = models.CharField(max_length=255)
        description = models.TextField(blank=True, null=True)
        price = models.FloatField()
        image = models.ImageField(upload_to='item_images', blank=True, null=True)
        is_sold = models.BooleanField(default=False)
        created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return self.name

class Person(models.Model):  
    name = models.CharField(max_length=100)  
    marks = models.CharField(max_length=100)  
    image = models.ImageField(upload_to='person_images/', blank=True, null=True)  
    email = models.EmailField(max_length=100, blank=True, null=True, validators=[EmailValidator]) 
    def __str__(self):  
        return self.name  
            