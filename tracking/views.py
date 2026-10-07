from django.shortcuts import render
from orders.models import Order

def track_order(request):
    order = None
    error = None
    
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        contact = request.POST.get('contact') # email or phone
        
        try:
            # Simple check for either email or phone
            order = Order.objects.get(tracking_code=tracking_code)
            if order.customer_email != contact and order.customer_phone != contact:
                order = None
                error = "Los datos de contacto no coinciden con este pedido."
        except Order.DoesNotExist:
            error = "Código de seguimiento no encontrado."
            
    return render(request, 'tracking/track.html', {'order': order, 'error': error})
