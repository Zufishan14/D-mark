from django.contrib import admin
from .models import Item
from .models import Category
# Register your models here.
admin.site.register(Category)
admin.site.register(Item)