from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product
from orders.models import Order, OrderItem


class TrackOrderTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Hombre', slug='hombre')
        product = Product.objects.create(
            category=category,
            name='Camisa',
            slug='camisa',
            description='Descripción',
            price='20.00',
            stock=2,
        )
        self.order = Order.objects.create(
            customer_name='Cliente',
            customer_email='cliente@example.com',
            customer_phone='+56912345678',
        )
        OrderItem.objects.create(order=self.order, product=product, price='20.00', quantity=1)

    def test_tracking_accepts_case_insensitive_code_and_email_without_exposing_contact(self):
        response = self.client.post(reverse('tracking:track'), {
            'tracking_code': self.order.tracking_code.lower(),
            'contact': 'CLIENTE@example.com',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Camisa')
        self.assertNotContains(response, self.order.customer_email)
        self.assertNotContains(response, self.order.customer_phone)

    def test_tracking_rejects_wrong_contact(self):
        response = self.client.post(reverse('tracking:track'), {
            'tracking_code': self.order.tracking_code,
            'contact': 'incorrect@example.com',
        })

        self.assertContains(response, 'no coinciden')
        self.assertNotContains(response, 'Camisa')

# Create your tests here.
