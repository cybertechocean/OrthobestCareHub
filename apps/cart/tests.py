from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from apps.products.models import Category, Product
from apps.cart.cart import Cart

class CartOperationsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Supports", slug="supports")
        self.product = Product.objects.create(
            name="Knee Support",
            sku="OBC-KS-001",
            category=self.category,
            price=Decimal("2500.00"),
            stock_quantity=10,
            is_available=True
        )

    def test_cart_add_ajax(self):
        response = self.client.post(
            reverse('cart:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2, 'ajax': '1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_count'], 2)

    def test_cart_view_renders(self):
        # Add item first
        self.client.post(
            reverse('cart:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 1}
        )
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Knee Support")
