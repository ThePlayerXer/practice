from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm

def catalog(request):
    products = Product.objects.filter(is_available=True)
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        products = products.filter(category__category_type=category)
    
    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Фильтрация по бренду
    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand__icontains=brand)
    
    # Сортировка
    sort = request.GET.get('sort', 'name_asc')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('name')
    
    return render(request, 'products/catalog.html', {
        'products': products,
        'categories': Category.objects.all()
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    cart_product_form = CartAddProductForm()
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })