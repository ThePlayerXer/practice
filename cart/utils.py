def get_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for product_id, item_data in cart.items():
        cart_items.append({
            'product_id': product_id,
            'quantity': item_data.get('quantity', 1),
            'price': item_data.get('price', 0),
        })
    return cart_items