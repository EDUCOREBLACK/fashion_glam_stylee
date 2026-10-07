from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    featured_products = Product.objects.filter(is_active=True)[:4]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category_list.html', context)
