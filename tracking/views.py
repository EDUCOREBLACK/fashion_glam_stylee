from django.shortcuts import render
from orders.models import Order

def track_order(request):
    order = None
    error = None
    
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code', '').strip()
        contact = request.POST.get('contact', '').strip()
        
        order = Order.objects.filter(tracking_code__iexact=tracking_code).first()
        if order and contact.casefold() not in {
            order.customer_email.casefold(),
            order.customer_phone.casefold(),
        }:
            order = None
            error = "Los datos de contacto no coinciden con este pedido."
        elif not order:
            error = "Código de seguimiento no encontrado."
            
    return render(request, 'tracking/track.html', {'order': order, 'error': error})
