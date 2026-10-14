from django.test import TestCase, override_settings
from django.urls import reverse
from catalog.models import Category, Product
from .models import Order, OrderItem
import urllib.parse

@override_settings(WHATSAPP_PHONE_NUMBER='56912345678')
class CheckoutAndWhatsAppFlowTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Hombre', slug='hombre')
        self.product = Product.objects.create(
            name='Test Shirt',
            slug='test-shirt',
            category=self.category,
            price=100.00,
            stock=10,
            is_active=True
        )
        self.checkout_url = reverse('orders:checkout', args=[self.product.slug])

    def test_checkout_creates_order_and_reduces_stock(self):
        # Enviar petición POST para finalizar pedido
        response = self.client.post(self.checkout_url, {
            'customer_name': 'Rene Villegas',
            'customer_email': 'rene@test.com',
            'customer_phone': '+56987654321',
            'quantity': 2
        })
        
        # Verificar que redirige a WhatsApp
        self.assertEqual(response.status_code, 302)
        self.assertTrue('wa.me' in response.url)
        
        # Verificar reducción de stock
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        
        # Verificar Orden creada
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.customer_name, 'Rene Villegas')
        self.assertTrue(order.tracking_code)
        
        # Verificar mensaje codificado de WhatsApp
        self.assertTrue(urllib.parse.quote(order.tracking_code) in response.url)

    def test_checkout_insufficient_stock(self):
        # Intentar comprar más del stock disponible
        response = self.client.post(self.checkout_url, {
            'customer_name': 'Rene Villegas',
            'customer_email': 'rene@test.com',
            'customer_phone': '+56987654321',
            'quantity': 20
        })
        
        # Verificar que vuelve al form con error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cantidad')
        
        # Stock no deducido y orden no creada
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(Order.objects.count(), 0)

    def test_checkout_rejects_missing_or_invalid_customer_data(self):
        response = self.client.post(self.checkout_url, {
            'customer_name': '   ',
            'customer_email': 'not-an-email',
            'customer_phone': 'bad',
            'quantity': 1
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

    @override_settings(WHATSAPP_PHONE_NUMBER='')
    def test_checkout_requires_configured_whatsapp_number(self):
        response = self.client.post(self.checkout_url, {
            'customer_name': 'Rene Villegas',
            'customer_email': 'rene@test.com',
            'customer_phone': '+56987654321',
            'quantity': 1
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no ha configurado su número de WhatsApp')
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(Order.objects.count(), 0)

    def test_checkout_rejects_invalid_quantity(self):
        response = self.client.post(self.checkout_url, {
            'customer_name': 'Rene Villegas',
            'customer_email': 'rene@test.com',
            'customer_phone': '+56987654321',
            'quantity': '-1'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'La cantidad debe ser al menos 1.')
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(Order.objects.count(), 0)
