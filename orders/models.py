from django.db import models
import uuid
from catalog.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('RECEIVED', 'Pedido Recibido'),
        ('PREPARING', 'En Preparación'),
        ('DISPATCHED', 'Despachado'),
        ('DELIVERED', 'Entregado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Encrypted fields could be used here via third-party packages if DB-level encryption is required
    # e.g., django-cryptography for strict Chilean Data Protection Law
    
    tracking_code = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.tracking_code} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Protect from deletion if ordered
    price = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of the price
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
