from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from catalog.models import Product
from .models import Order, OrderItem
import urllib.parse
from django.db import transaction

def checkout_product(request, slug):
    # Fetch original without lock just for GET requests
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        quantity = int(request.POST.get('quantity', 1))
        
        with transaction.atomic():
            # Lock the row for update to prevent race conditions (doble reserva)
            locked_product = Product.objects.select_for_update().get(id=product.id)
            
            # Validar stock básico
            if locked_product.stock < quantity:
                return render(request, 'orders/checkout.html', {'product': locked_product, 'error': 'Stock insuficiente o acaba de agotarse.'})
                
            # Crear la orden
            order = Order.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                status='RECEIVED'
            )
            
            # Crear item
            OrderItem.objects.create(
                order=order,
                product=locked_product,
                price=locked_product.price,
                quantity=quantity
            )
            
            # Deducir stock de forma segura
            locked_product.stock -= quantity
            locked_product.save()
            
        # Generar enlace de WhatsApp (fuera de la transacción)
        phone_number = "56912345678" # Reemplazar con el número de la tienda
        message = f"Hola Fashion Glam Stylee! ✨\n\nQuiero confirmar mi pedido:\n"
        message += f"🛍️ Producto: {locked_product.name} ({locked_product.brand})\n"
        message += f"📦 Cantidad: {quantity}\n"
        message += f"💵 Total: ${locked_product.price * quantity}\n\n"
        message += f"Mi código de seguimiento es: *{order.tracking_code}*\n"
        message += f"Nombre: {customer_name}\n"
        message += f"¿Me indican los pasos para realizar la transferencia/pago?"
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
        
        return redirect(whatsapp_url)
        
    return render(request, 'orders/checkout.html', {'product': product})
