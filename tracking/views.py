from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from orders.models import Order


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def track_order(request):
    order = None
    error = None
    
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code', '').strip()
        contact = request.POST.get('contact', '').strip()
        
        order = Order.objects.filter(tracking_code__iexact=tracking_code).first()
        if not order or contact.casefold() not in {
            order.customer_email.casefold(),
            order.customer_phone.casefold(),
        }:
            order = None
            error = "No se encontró un pedido con esos datos."
            
    return render(request, 'tracking/track.html', {'order': order, 'error': error})
