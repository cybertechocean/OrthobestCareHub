from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from apps.products.models import Product, ProductVariant
from .cart import Cart


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        recent_ids = request.session.get('recently_viewed', [])[:4]
        if recent_ids:
            recent_products_dict = {p.id: p for p in Product.objects.filter(id__in=recent_ids, is_available=True).select_related('category').prefetch_related('images')}
            recently_viewed_products = [recent_products_dict[pid] for pid in recent_ids if pid in recent_products_dict]
        else:
            recently_viewed_products = []

        return render(request, "cart/cart_detail.html", {
            'cart': cart,
            'cart_items': list(cart),
            'cart_subtotal': cart.get_subtotal(),
            'recently_viewed_products': recently_viewed_products,
        })


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id, is_available=True)
        
        variant_id = request.POST.get('variant_id')
        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product, is_available=True)
            except ProductVariant.DoesNotExist:
                pass

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        override = request.POST.get('override') == 'true'
        actual_qty = cart.add(product=product, variant=variant, quantity=quantity, override_quantity=override)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == '1':
            img_url = product.primary_image.image.url if (product.primary_image and product.primary_image.image) else '/static/images/placeholder.jpg'
            price = variant.effective_price if variant else product.price
            return JsonResponse({
                'success': True,
                'message': f"'{product.name}' added to your cart!",
                'cart_total_count': len(cart),
                'cart_subtotal': f"KSh {cart.get_subtotal():,.0f}",
                'product_name': product.name,
                'product_price': f"KSh {price:,.0f}",
                'product_image': img_url,
                'quantity': actual_qty,
            })

        messages.success(request, f"'{product.name}' was added to your cart.")
        
        # If "Buy Now" clicked, redirect straight to checkout
        if request.POST.get('action') == 'buy_now':
            return redirect('orders:checkout')

        return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, item_key):
        cart = Cart(request)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        cart.update_quantity(item_key, quantity)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Calculate item specific total
            item_total = 0
            for item in cart:
                if item['key'] == item_key:
                    item_total = item['total_price']
                    break

            return JsonResponse({
                'success': True,
                'cart_total_count': len(cart),
                'cart_subtotal': f"KSh {cart.get_subtotal():,.0f}",
                'item_total': f"KSh {item_total:,.0f}",
            })

        return redirect('cart:cart_detail')


class CartRemoveView(View):
    def post(self, request, item_key):
        cart = Cart(request)
        cart.remove(item_key)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': "Item removed from cart",
                'cart_total_count': len(cart),
                'cart_subtotal': f"KSh {cart.get_subtotal():,.0f}",
            })

        messages.info(request, "Item removed from your cart.")
        return redirect('cart:cart_detail')


class CartClearView(View):
    def post(self, request):
        cart = Cart(request)
        cart.clear()
        messages.info(request, "Your cart has been cleared.")
        return redirect('cart:cart_detail')
