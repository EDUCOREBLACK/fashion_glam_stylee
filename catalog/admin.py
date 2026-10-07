from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'stock', 'is_active', 'gender']
    list_filter = ['is_active', 'gender', 'brand', 'category']
    search_fields = ['name', 'brand']
    prepopulated_fields = {'slug': ('name',)}
