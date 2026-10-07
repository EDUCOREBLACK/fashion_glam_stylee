import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from catalog.models import Category, Product

def populate():
    print("Agregando nuevos productos con imagenes reales...")
    
    # Categories
    cat_mujer, _ = Category.objects.get_or_create(name='Mujer', slug='mujer')
    cat_hombre, _ = Category.objects.get_or_create(name='Hombre', slug='hombre')

    # Delete old fake products if we want a clean slate, or just add new ones.
    from orders.models import OrderItem, Order
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()

    products = [
        {
            'name': 'Conjunto Calvin Klein Blanco',
            'slug': 'ck-white-set',
            'brand': 'Calvin Klein',
            'category': cat_mujer,
            'description': 'Clásico conjunto Calvin Klein de algodón elástico en color blanco. Iconic logo tape.',
            'price': 65.00,
            'stock': 10,
            'gender': 'W',
            'image': 'products/ck_white_set.jpg'
        },
        {
            'name': 'Conjunto Calvin Klein Negro (Jennie Edition)',
            'slug': 'ck-black-set',
            'brand': 'Calvin Klein',
            'category': cat_mujer,
            'description': 'Exclusivo conjunto negro con detalles premium. Diseño moderno y soporte perfecto.',
            'price': 75.00,
            'stock': 5,
            'gender': 'W',
            'image': 'products/ck_black_set.png'
        },
        {
            'name': 'Panty Calvin Klein Gris',
            'slug': 'ck-grey-panty',
            'brand': 'Calvin Klein',
            'category': cat_mujer,
            'description': 'Panty clásica gris de algodón con el inconfundible logo Calvin Klein.',
            'price': 25.00,
            'stock': 20,
            'gender': 'W',
            'image': 'products/ck_grey_panty.png'
        },
        {
            'name': 'Panty Calvin Klein Roja',
            'slug': 'ck-red-panty',
            'brand': 'Calvin Klein',
            'category': cat_mujer,
            'description': 'Panty roja vibrante para destacar. Comodidad y estilo en una sola pieza.',
            'price': 25.00,
            'stock': 15,
            'gender': 'W',
            'image': 'products/ck_red_panty.png'
        },
        {
            'name': 'Conjunto Tommy Hilfiger Rojo',
            'slug': 'th-red-set',
            'brand': 'Tommy Hilfiger',
            'category': cat_mujer,
            'description': 'Conjunto rojo vibrante con el clásico logo de Tommy Hilfiger en la banda elástica.',
            'price': 60.00,
            'stock': 8,
            'gender': 'W',
            'image': 'products/th_red_set.png'
        },
        {
            'name': 'Pack 3 Boxers Tommy Hilfiger',
            'slug': 'th-boxer-pack',
            'brand': 'Tommy Hilfiger',
            'category': cat_hombre,
            'description': 'Pack de 3 boxers clásicos de algodón (Negro, Azul Marino, Gris). Ajuste perfecto.',
            'price': 55.00,
            'stock': 25,
            'gender': 'M',
            'image': 'products/th_boxers.png'
        }
    ]

    for p_data in products:
        Product.objects.create(**p_data)

    print("Catálogo actualizado exitosamente con las nuevas imágenes.")

if __name__ == '__main__':
    populate()
