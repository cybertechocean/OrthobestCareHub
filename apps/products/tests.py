from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.products.models import Category, Product, ProductVariant, ProductReview, Wishlist, WishlistItem

User = get_user_model()

class ProductModelAndViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="Mobility Aids", slug="mobility-aids")
        self.product = Product.objects.create(
            name="Manual Wheelchair Pro",
            sku="OBC-MW-999",
            category=self.category,
            price=Decimal("12500.00"),
            compare_at_price=Decimal("15000.00"),
            stock_quantity=5,
            is_available=True,
            short_description="High quality test wheelchair"
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            name="Size: 18 Inch",
            price_adjustment=Decimal("500.00"),
            stock_quantity=3
        )

    def test_product_creation_and_properties(self):
        self.assertEqual(self.product.slug, "manual-wheelchair-pro")
        self.assertTrue(self.product.in_stock)
        self.assertTrue(self.product.is_on_sale)
        self.assertEqual(self.product.discount_percentage, 17)
        self.assertEqual(self.variant.effective_price, Decimal("13000.00"))

    def test_shop_view(self):
        response = self.client.get(reverse('products:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manual Wheelchair Pro")

    def test_category_view(self):
        response = self.client.get(reverse('products:category_detail', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manual Wheelchair Pro")

    def test_product_detail_and_browsing_history(self):
        # Visit product detail
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manual Wheelchair Pro")
        self.assertContains(response, "KSh 12,500")
        
        # Verify product is recorded in session browsing history
        self.assertIn(self.product.id, self.client.session['recently_viewed'])

    def test_clear_browsing_history(self):
        # Seed session history
        session = self.client.session
        session['recently_viewed'] = [self.product.id]
        session.save()

        response = self.client.post(reverse('products:clear_history'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('recently_viewed', self.client.session)

    def test_wishlist_guest_toggle_and_view(self):
        # 1. Guest toggle add
        response = self.client.post(
            reverse('products:wishlist_toggle', kwargs={'product_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['in_wishlist'])
        self.assertEqual(data['total_count'], 1)

        # 2. View wishlist page
        page_response = self.client.get(reverse('products:wishlist'))
        self.assertEqual(page_response.status_code, 200)
        self.assertContains(page_response, "Manual Wheelchair Pro")

        # 3. Guest toggle remove
        response_remove = self.client.post(
            reverse('products:wishlist_toggle', kwargs={'product_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response_remove.status_code, 200)
        data_remove = response_remove.json()
        self.assertFalse(data_remove['in_wishlist'])
        self.assertEqual(data_remove['total_count'], 0)

    def test_wishlist_authenticated_persistence(self):
        self.client.login(username="testuser", password="password123")
        
        # Add to wishlist
        response = self.client.post(
            reverse('products:wishlist_toggle', kwargs={'product_id': self.product.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['in_wishlist'])
        
        # Verify in DB
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(wishlist.items.count(), 1)

        # Move to cart
        move_response = self.client.post(
            reverse('products:wishlist_move_to_cart', kwargs={'product_id': self.product.id})
        )
        self.assertEqual(move_response.status_code, 302)
        self.assertEqual(wishlist.items.count(), 0)

    def test_product_live_search(self):
        response = self.client.get(f"{reverse('products:live_search')}?q=Wheelchair")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['sku'], "OBC-MW-999")
