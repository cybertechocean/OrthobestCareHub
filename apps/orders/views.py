from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from apps.cart.cart import Cart
from .models import Order, OrderItem, DeliveryZone, Coupon, OrderStatusHistory
from .forms import CheckoutForm, OrderTrackForm, normalize_kenyan_phone


class CheckoutView(View):
    def get(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.warning(request, "Your cart is currently empty. Please add products before checking out.")
            return redirect('products:shop')

        zones = DeliveryZone.objects.filter(is_active=True)
        default_zone = zones.first()
        
        # Pre-fill user details if logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['first_name'] = request.user.first_name
            initial_data['last_name'] = request.user.last_name
            initial_data['email'] = request.user.email
            if hasattr(request.user, 'profile'):
                initial_data['phone'] = request.user.profile.phone
                initial_data['county'] = request.user.profile.county
                initial_data['town_city'] = request.user.profile.town_city
                initial_data['estate_address'] = request.user.profile.address

        form = CheckoutForm(initial=initial_data)
        subtotal = cart.get_subtotal()
        delivery_fee = default_zone.delivery_fee if default_zone else Decimal('0.00')
        total = subtotal + delivery_fee

        return render(request, "orders/checkout.html", {
            'form': form,
            'cart': cart,
            'cart_items': list(cart),
            'subtotal': subtotal,
            'delivery_zones': zones,
            'default_zone': default_zone,
            'delivery_fee': delivery_fee,
            'total': total,
        })

    def post(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.warning(request, "Your cart is empty.")
            return redirect('products:shop')

        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user

                # Calculate Subtotal from fresh cart
                subtotal = Decimal(str(cart.get_subtotal()))
                order.subtotal = subtotal

                # Calculate Delivery Fee from selected zone
                delivery_zone = form.cleaned_data.get('delivery_zone')
                delivery_fee = delivery_zone.delivery_fee if delivery_zone else Decimal('0.00')
                order.delivery_fee = delivery_fee

                # Process Coupon Code if provided
                coupon_code = form.cleaned_data.get('coupon_code', '').strip().upper()
                discount_amount = Decimal('0.00')
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(code=coupon_code, active=True)
                        discount_amount = coupon.calculate_discount(subtotal)
                        order.coupon_code = coupon.code
                        order.discount_amount = discount_amount
                        coupon.times_used += 1
                        coupon.save()
                    except Coupon.DoesNotExist:
                        pass

                # Final Total Calculation
                order.total_amount = max(subtotal + delivery_fee - discount_amount, Decimal('0.00'))
                order.save()

                # Create Order Items and adjust stock
                for item in cart:
                    product = item['product']
                    variant = item['variant']
                    quantity = item['quantity']
                    price = item['price']
                    total_price = item['total_price']

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        variant_name=variant.name if variant else '',
                        sku=product.sku if not variant else f"{product.sku}{variant.sku_modifier}",
                        unit_price=price,
                        quantity=quantity,
                        total_price=total_price
                    )

                    # Deduct stock safely
                    if variant:
                        variant.stock_quantity = max(0, variant.stock_quantity - quantity)
                        variant.save()
                    else:
                        product.stock_quantity = max(0, product.stock_quantity - quantity)
                        product.save()

                # Initial status history record
                OrderStatusHistory.objects.create(
                    order=order,
                    status='pending',
                    notes='Order placed successfully.'
                )

                # Clear cart
                cart.clear()

                # Route to payment processing
                return redirect('payments:process', order_number=order.order_number)

        # Form had validation errors
        zones = DeliveryZone.objects.filter(is_active=True)
        subtotal = cart.get_subtotal()
        return render(request, "orders/checkout.html", {
            'form': form,
            'cart': cart,
            'cart_items': list(cart),
            'subtotal': subtotal,
            'delivery_zones': zones,
            'delivery_fee': Decimal('0.00'),
            'total': subtotal,
        })


class CouponValidateAjaxView(View):
    def post(self, request):
        code = request.POST.get('code', '').strip().upper()
        subtotal_raw = request.POST.get('subtotal', '0')
        try:
            subtotal = Decimal(str(subtotal_raw))
        except Exception:
            subtotal = Decimal('0.00')

        try:
            coupon = Coupon.objects.get(code=code, active=True)
            if coupon.minimum_order > subtotal:
                return JsonResponse({
                    'success': False,
                    'message': f"Coupon requires a minimum order of KSh {coupon.minimum_order:,.0f}."
                })
            discount = coupon.calculate_discount(subtotal)
            return JsonResponse({
                'success': True,
                'discount_amount': float(discount),
                'discount_formatted': f"KSh {discount:,.0f}",
                'message': f"Coupon '{coupon.code}' applied successfully!"
            })
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': "Invalid or expired coupon code."
            })


class OrderConfirmationView(TemplateView):
    template_name = "orders/order_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = self.kwargs.get('order_number')
        order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
        context['order'] = order

        # WhatsApp CTA with order number
        import urllib.parse
        wa_text = f"Hello Orthobest Care Hub, I have placed order #{order.order_number} for KSh {order.total_amount:,.0f}. Please confirm receipt."
        context['whatsapp_order_url'] = f"https://wa.me/254798246811?text={urllib.parse.quote(wa_text)}"
        return context


class OrderTrackingView(View):
    template_name = "orders/order_track.html"

    def get(self, request):
        form = OrderTrackForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderTrackForm(request.POST)
        order = None
        if form.is_valid():
            order_number = form.cleaned_data['order_number'].strip().upper()
            contact_input = form.cleaned_data['phone_or_email'].strip()
            
            # Normalize if phone
            normalized_phone = normalize_kenyan_phone(contact_input)

            # Query order by number and matching either phone or email
            orders = Order.objects.filter(order_number=order_number)
            for o in orders:
                if o.email.lower() == contact_input.lower() or normalize_kenyan_phone(o.phone) == normalized_phone:
                    order = o
                    break

            if not order:
                messages.error(request, f"No order found matching #{order_number} and provided contact details.")
        return render(request, self.template_name, {'form': form, 'order': order})


class OrderDetailView(View):
    def get(self, request, order_number):
        order = get_object_or_404(Order.objects.prefetch_related('items', 'status_history'), order_number=order_number)
        # Security check: if user is logged in, ensure they own the order unless staff
        if request.user.is_authenticated and not request.user.is_staff:
            if order.user and order.user != request.user:
                raise Http404("Order not found.")
        return render(request, "orders/order_detail.html", {'order': order})
