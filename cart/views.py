from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from orders.models import Order, OrderItem

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_items = 0
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = item_data.get('quantity', 1)
            price = float(item_data.get('price', product.get_final_price()))
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'get_total_price': lambda p=price, q=quantity: p * q,
            })
            
            total_price += price * quantity
            total_items += quantity
        except (Product.DoesNotExist, ValueError, KeyError):
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
            'price': str(product.get_final_price()),
            'name': product.name,
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product = get_object_or_404(Product, id=product_id)
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'Товар "{product.name}" удален из корзины')
    
    return redirect('cart:cart_detail')

def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart and quantity > 0:
            cart[product_id_str]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Корзина обновлена')
    
    return redirect('cart:cart_detail')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            payment_method=request.POST.get('payment_method'),
            total_price=0  # Временно 0, посчитаем ниже
        )
        
        total_price = 0
        
        # Добавляем товары в заказ
        for product_id, item_data in cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                quantity = item_data.get('quantity', 1)
                price = float(item_data.get('price', product.get_final_price()))
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=price,
                    quantity=quantity
                )
                
                total_price += price * quantity
                
                # Уменьшаем количество товара на складе
                if product.stock >= quantity:
                    product.stock -= quantity
                    product.save()
                
            except (Product.DoesNotExist, ValueError, KeyError):
                continue
        
        # Обновляем итоговую цену заказа
        order.total_price = total_price
        order.save()
        
        # Очищаем корзину
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f'Заказ #{order.order_number} успешно оформлен!')
        return redirect('users:orders')
    
    # Рассчитываем итоговую стоимость
    total_price = 0
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = item_data.get('quantity', 1)
            price = float(item_data.get('price', product.get_final_price()))
            total_price += price * quantity
        except (Product.DoesNotExist, ValueError, KeyError):
            continue
    
    return render(request, 'cart/checkout.html', {
        'total_price': total_price,
        'cart_items_count': len(cart)
    })