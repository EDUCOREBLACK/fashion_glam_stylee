from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'customer_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tracking_code', 'customer_name', 'customer_email']
    readonly_fields = ['tracking_code']
    inlines = [OrderItemInline]
