from django.shortcuts import render
from products.models import Product

def home(request):
    popular_products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'home.html', {
        'popular_products': popular_products
    })

def about(request):
    return render(request, 'pages/about.html')

def contacts(request):
    return render(request, 'pages/contacts.html')