from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from apps.products.models import Category, Product, ProductVariant, ProductReview

class ProductModelAndViewsTest(TestCase):
    def setUp(self):
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

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manual Wheelchair Pro")
        self.assertContains(response, "KSh 12,500")

    def test_product_live_search(self):
        response = self.client.get(f"{reverse('products:live_search')}?q=Wheelchair")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['sku'], "OBC-MW-999")
