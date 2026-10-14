from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    search_fields = ['name', 'slug']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_product_count=Count('products'))

    @admin.display(description='Productos')
    def product_count(self, obj):
        return obj._product_count

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'image_preview', 'price', 'stock', 'is_active', 'gender']
    list_filter = ['is_active', 'gender', 'brand', 'category']
    search_fields = ['name', 'brand', 'slug', 'description']
    list_editable = ['stock', 'is_active']
    list_select_related = ['category']
    autocomplete_fields = ['category']
    ordering = ['name']
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '—'
    readonly_fields = ['image_preview']
    fieldsets = [
        ('Información del producto', {
            'fields': ['name', 'slug', 'brand', 'category', 'gender'],
        }),
        ('Precio y disponibilidad', {
            'fields': ['price', 'stock', 'is_active'],
        }),
        ('Descripción e imagen', {
            'fields': ['description', 'image', 'image_preview'],
        }),
    ]

    @admin.action(description='Activar productos seleccionados')
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Desactivar productos seleccionados')
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)

    actions = ['activate_selected', 'deactivate_selected']

    @admin.display(description='Imagen')
    def image_preview(self, obj):
        if not obj or not obj.image:
            return 'Sin imagen'
        return format_html(
            '<img src="{}" alt="{}" style="width:48px;height:64px;object-fit:cover;">',
            obj.image.url,
            obj.name,
        )
