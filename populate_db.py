import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from catalog.models import Category, Product

def populate():
    print("Populating database...")
    
    # Categories
    cat_mujer, _ = Category.objects.get_or_create(name='Mujer', slug='mujer')
    cat_hombre, _ = Category.objects.get_or_create(name='Hombre', slug='hombre')
    cat_lenceria, _ = Category.objects.get_or_create(name='Lencería Premium', slug='lenceria-premium')

    # Products
    products = [
        {
            'name': 'Bralette de Encaje Fino',
            'slug': 'bralette-encaje-fino-ck',
            'brand': 'Calvin Klein',
            'category': cat_lenceria,
            'description': 'Bralette con diseño minimalista y encaje francés de alta calidad. Comodidad y lujo.',
            'price': 45.99,
            'stock': 10,
            'gender': 'W'
        },
        {
            'name': 'Boxer Brief Classic',
            'slug': 'boxer-brief-classic-th',
            'brand': 'Tommy Hilfiger',
            'category': cat_hombre,
            'description': 'Boxer clásico de algodón elástico con banda elástica distintiva de la marca.',
            'price': 35.00,
            'stock': 25,
            'gender': 'M'
        },
        {
            'name': 'Conjunto Seda Nocturna',
            'slug': 'conjunto-seda-nocturna',
            'brand': 'Calvin Klein',
            'category': cat_lenceria,
            'description': 'Conjunto de seda premium para un confort absoluto con detalles translúcidos.',
            'price': 89.99,
            'stock': 5,
            'gender': 'W'
        },
        {
            'name': 'Camisa Oxford Blanca',
            'slug': 'camisa-oxford-blanca-th',
            'brand': 'Tommy Hilfiger',
            'category': cat_hombre,
            'description': 'Camisa Oxford de corte recto y algodón puro. Ideal para un look sofisticado.',
            'price': 120.00,
            'stock': 15,
            'gender': 'M'
        }
    ]

    for p_data in products:
        Product.objects.get_or_create(
            slug=p_data['slug'],
            defaults=p_data
        )

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
