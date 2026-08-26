from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from apps.products.models import Category, Product
from apps.orders.models import DeliveryZone, Coupon, Order, OrderItem
from apps.orders.forms import normalize_kenyan_phone

class OrderAndCheckoutTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Mobility", slug="mobility")
        self.product = Product.objects.create(
            name="Walking Cane",
            sku="OBC-WC-001",
            category=self.category,
            price=Decimal("1800.00"),
            stock_quantity=10,
            is_available=True
        )
        self.zone = DeliveryZone.objects.create(
            name="Nairobi CBD",
            delivery_fee=Decimal("200.00"),
            is_active=True
        )
        self.coupon = Coupon.objects.create(
            code="SAVE10",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            minimum_order=Decimal("1000.00"),
            active=True
        )

    def test_phone_normalization(self):
        self.assertEqual(normalize_kenyan_phone("0719160398"), "254719160398")
        self.assertEqual(normalize_kenyan_phone("+254 719 160 398"), "254719160398")
        self.assertEqual(normalize_kenyan_phone("0110 123 456"), "254110123456")

    def test_coupon_discount_calculation(self):
        discount = self.coupon.calculate_discount(Decimal("2000.00"))
        self.assertEqual(discount, Decimal("200.00"))

    def test_checkout_flow(self):
        # Add to cart
        self.client.post(reverse('cart:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 2})

        # Post Checkout
        response = self.client.post(reverse('orders:checkout'), {
            'first_name': 'Amina',
            'last_name': 'Hassan',
            'phone': '0719160398',
            'email': 'amina@example.com',
            'county': 'Nairobi',
            'town_city': 'Nairobi CBD',
            'estate_address': 'Mfangano St, Room 12',
            'delivery_zone': self.zone.id,
            'coupon_code': 'SAVE10',
            'payment_method': 'mpesa'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify Order was created
        order = Order.objects.get(phone='254719160398')
        self.assertEqual(order.subtotal, Decimal("3600.00"))
        self.assertEqual(order.delivery_fee, Decimal("200.00"))
        self.assertEqual(order.discount_amount, Decimal("360.00"))
        self.assertEqual(order.total_amount, Decimal("3440.00"))
        self.assertEqual(order.items.count(), 1)
        
        # Check stock deduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 8)
