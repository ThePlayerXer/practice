from django.shortcuts import render
from .models import Product

def catalog(request):
    products = Product.objects.all()
    return render(request, 'products/catalog.html', {'products': products})
