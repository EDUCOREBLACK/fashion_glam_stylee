from django.contrib import admin
from django.utils import timezone
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ['product', 'price', 'quantity']
    fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'customer_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tracking_code', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['tracking_code', 'customer_name', 'customer_email', 'customer_phone', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = [
        ('Pedido', {'fields': ['tracking_code', 'status', 'created_at', 'updated_at']}),
        ('Cliente', {'fields': ['customer_name', 'customer_email', 'customer_phone']}),
    ]
    inlines = [OrderItemInline]

    @admin.action(description='Marcar pedidos seleccionados en preparación')
    def mark_as_preparing(self, request, queryset):
        queryset.update(status='PREPARING', updated_at=timezone.now())

    actions = ['mark_as_preparing']
