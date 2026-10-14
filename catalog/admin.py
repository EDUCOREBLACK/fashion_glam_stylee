from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Productos')
    def product_count(self, obj):
        return obj.products.count()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'image_preview', 'price', 'stock', 'is_active', 'gender']
    list_filter = ['is_active', 'gender', 'brand', 'category']
    search_fields = ['name', 'brand', 'slug', 'description']
    list_editable = ['stock', 'is_active']
    list_select_related = ['category']
    autocomplete_fields = ['category']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Imagen')
    def image_preview(self, obj):
        if not obj.image:
            return 'Sin imagen'
        return format_html(
            '<img src="{}" alt="{}" style="width:48px;height:64px;object-fit:cover;">',
            obj.image.url,
            obj.name,
        )
