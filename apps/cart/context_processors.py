from .cart import Cart

def cart_context(request):
    try:
        cart = Cart(request)
        cart_items_list = list(cart)
        return {
            'cart': cart,
            'cart_items': cart_items_list,
            'cart_total_count': len(cart),
            'cart_subtotal': cart.get_subtotal(),
        }
    except Exception:
        return {
            'cart': None,
            'cart_items': [],
            'cart_total_count': 0,
            'cart_subtotal': 0,
        }
