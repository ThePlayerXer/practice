from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_items = 0
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = item_data.get('quantity', 1)
            price = float(item_data.get('price', 0))
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'get_total_price': lambda p=price, q=quantity: p * q,
            })
            
            total_price += price * quantity
            total_items += quantity
        except (Product.DoesNotExist, ValueError):
            continue
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': str(product.price),
            'name': product.name,
        }
    
    request.session['cart'] = cart
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    
    return redirect('cart:cart_detail')

def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart and quantity > 0:
            cart[product_id_str]['quantity'] = quantity
            request.session['cart'] = cart
    
    return redirect('cart:cart_detail')
