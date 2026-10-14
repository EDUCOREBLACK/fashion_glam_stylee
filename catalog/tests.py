from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Category, Product


class CatalogViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Mujer', slug='mujer')
        self.product = Product.objects.create(
            category=self.category,
            name='Producto visible',
            slug='producto-visible',
            description='Descripción',
            price='25.00',
            stock=3,
        )
        self.hidden_product = Product.objects.create(
            category=self.category,
            name='Producto oculto',
            slug='producto-oculto',
            description='Descripción',
            price='30.00',
            stock=3,
            is_active=False,
        )

    def test_home_and_category_only_show_active_products(self):
        home = self.client.get(reverse('home'))
        category = self.client.get(reverse('catalog:category', args=[self.category.slug]))

        self.assertEqual(home.status_code, 200)
        self.assertEqual(list(home.context['featured_products']), [self.product])
        self.assertEqual(category.status_code, 200)
        self.assertEqual(list(category.context['products']), [self.product])

    def test_product_detail_excludes_inactive_related_products(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.product.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['related_products']), [])

    def test_inactive_product_is_not_public(self):
        response = self.client.get(reverse('catalog:product_detail', args=[self.hidden_product.slug]))

        self.assertEqual(response.status_code, 404)


class ProductAdminTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Mujer', slug='mujer')
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='strong-test-password',
        )
        self.client.force_login(self.admin_user)

    def test_admin_can_create_product_with_image_field_available(self):
        add_url = reverse('admin:catalog_product_add')
        response = self.client.get(add_url)

        self.assertContains(response, 'id_image')
        self.assertContains(response, 'id_category')

        image_data = BytesIO()
        Image.new('RGB', (8, 8), color='red').save(image_data, format='PNG')
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            response = self.client.post(add_url, {
                'name': 'Producto nuevo',
                'slug': 'producto-nuevo',
                'brand': 'Marca',
                'category': self.category.pk,
                'description': 'Descripción',
                'price': '49.99',
                'stock': '8',
                'gender': 'U',
                'is_active': 'on',
                'image': SimpleUploadedFile(
                    'producto.png',
                    image_data.getvalue(),
                    content_type='image/png',
                ),
            })

            self.assertEqual(response.status_code, 302)
            product = Product.objects.get(slug='producto-nuevo')
            self.assertTrue(product.image)
            self.assertTrue(product.image.storage.exists(product.image.name))
            change_url = reverse('admin:catalog_product_change', args=[product.pk])
            self.assertContains(self.client.get(change_url), product.image.name)
