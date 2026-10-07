from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('coleccion/<slug:slug>/', views.category_list, name='category'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
]
