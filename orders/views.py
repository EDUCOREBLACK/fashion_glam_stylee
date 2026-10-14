from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from catalog.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm
import urllib.parse
from django.db import transaction
from django.db.models import F

def checkout_product(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method == 'POST':
        if not settings.WHATSAPP_PHONE_NUMBER:
            return render(request, 'orders/checkout.html', {
                'product': product,
                'form': CheckoutForm(request.POST, product=product),
                'error': 'La tienda aún no ha configurado su número de WhatsApp. Inténtalo más tarde.',
            })

        form = CheckoutForm(request.POST, product=product)
        if not form.is_valid():
            return render(request, 'orders/checkout.html', {'product': product, 'form': form})

        customer_name = form.cleaned_data['customer_name']
        customer_email = form.cleaned_data['customer_email']
        customer_phone = form.cleaned_data['customer_phone']
        quantity = form.cleaned_data['quantity']

        with transaction.atomic():
            locked_product = Product.objects.select_for_update().get(id=product.id)
            stock_reserved = Product.objects.filter(
                id=locked_product.id,
                stock__gte=quantity,
            ).update(stock=F('stock') - quantity)
            if not stock_reserved:
                form.add_error(None, 'Stock insuficiente o acaba de agotarse.')
                return render(request, 'orders/checkout.html', {'product': locked_product, 'form': form})

            order = Order.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                status='RECEIVED'
            )

            OrderItem.objects.create(
                order=order,
                product=locked_product,
                price=locked_product.price,
                quantity=quantity
            )

        message = f"Hola Fashion Glam Stylee! ✨\n\nQuiero confirmar mi pedido:\n"
        message += f"🛍️ Producto: {locked_product.name} ({locked_product.brand})\n"
        message += f"📦 Cantidad: {quantity}\n"
        message += f"💵 Total: ${locked_product.price * quantity}\n\n"
        message += f"Mi código de seguimiento es: *{order.tracking_code}*\n"
        message += f"Nombre: {customer_name}\n"
        message += f"¿Me indican los pasos para realizar la transferencia/pago?"
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{settings.WHATSAPP_PHONE_NUMBER}?text={encoded_message}"
        
        return redirect(whatsapp_url)

    return render(request, 'orders/checkout.html', {
        'product': product,
        'form': CheckoutForm(product=product),
        'error': 'Este producto está agotado.' if product.stock < 1 else None,
    })
