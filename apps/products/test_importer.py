import os
import tempfile
from decimal import Decimal
from django.test import TestCase
from django.core.management import call_command
from apps.products.models import Product, Category
from apps.products.management.commands.import_woocommerce import (
    clean_val,
    parse_price,
    resolve_price,
    resolve_stock,
    resolve_category_slugs,
    WOOCOMMERCE_CATEGORY_MAP,
)


class WooCommerceImporterUnitTest(TestCase):

    def test_clean_val_null_conversion(self):
        """Verify literal 'NULL', 'null', whitespace, and empty strings become None."""
        self.assertIsNone(clean_val("NULL"))
        self.assertIsNone(clean_val("null"))
        self.assertIsNone(clean_val("Null"))
        self.assertIsNone(clean_val(""))
        self.assertIsNone(clean_val("   "))
        self.assertIsNone(clean_val(None))
        self.assertEqual(clean_val("  OBC-123  "), "OBC-123")

    def test_parse_price(self):
        """Verify price parsing strips currency symbols, commas, and handles invalid numbers."""
        self.assertEqual(parse_price("10,000.00"), Decimal("10000.00"))
        self.assertEqual(parse_price("KSh 2,500"), Decimal("2500"))
        self.assertEqual(parse_price("KES 1800.50"), Decimal("1800.50"))
        self.assertIsNone(parse_price("NULL"))
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price("invalid"))
        self.assertIsNone(parse_price("-500"))

    def test_price_selection_and_compare_at_price(self):
        """Verify current_price priority and conditional compare_at_price."""
        # 1. Normal current_price with regular_price > current_price (valid sale)
        p, cmp_p, on_sale = resolve_price("8500", "10000", "8500")
        self.assertEqual(p, Decimal("8500"))
        self.assertEqual(cmp_p, Decimal("10000"))
        self.assertTrue(on_sale)

        # 2. current_price == regular_price (not on sale, compare_at_price must be None)
        p, cmp_p, on_sale = resolve_price("10000", "10000", "9500")
        self.assertEqual(p, Decimal("10000"))
        self.assertIsNone(cmp_p)
        self.assertFalse(on_sale)

        # 3. current_price is NULL, fallback to regular_price
        p, cmp_p, on_sale = resolve_price("NULL", "5000", "4500")
        self.assertEqual(p, Decimal("5000"))
        self.assertIsNone(cmp_p)
        self.assertFalse(on_sale)

        # 4. current_price & regular_price NULL, fallback to sale_price
        p, cmp_p, on_sale = resolve_price("NULL", "NULL", "3500")
        self.assertEqual(p, Decimal("3500"))
        self.assertIsNone(cmp_p)

        # 5. Missing all prices -> None (must be skipped)
        p, cmp_p, on_sale = resolve_price("NULL", "NULL", "NULL")
        self.assertIsNone(p)

    def test_known_exception_product_21503(self):
        """Product 21503 must have price 10000 and compare_at_price None (not on sale)."""
        p, cmp_p, on_sale = resolve_price("10000", "10000", "9150", wc_id=21503)
        self.assertEqual(p, Decimal("10000.00"))
        self.assertIsNone(cmp_p)
        self.assertFalse(on_sale)

    def test_stock_resolution(self):
        """Verify stock management and availability resolution."""
        # Managed stock with positive quantity
        managed, qty, avail = resolve_stock("yes", "instock", "12")
        self.assertTrue(managed)
        self.assertEqual(qty, 12)
        self.assertTrue(avail)

        # Unmanaged stock
        managed, qty, avail = resolve_stock("no", "instock", "NULL")
        self.assertFalse(managed)
        self.assertEqual(qty, 0)
        self.assertTrue(avail)

        # Out of stock
        managed, qty, avail = resolve_stock("yes", "outofstock", "0")
        self.assertTrue(managed)
        self.assertEqual(qty, 0)
        self.assertFalse(avail)

    def test_category_mapping_and_deduplication(self):
        """Verify category name normalization, mapping, and deduplication."""
        # Orthopaedic Appliances and Supports & Braces map to same Django category: orthopedic-supports
        raw_cats = ["Orthopaedic Appliances", "Supports & Braces"]
        mapped = resolve_category_slugs(99999, raw_cats)
        self.assertEqual(mapped, ["orthopedic-supports"])

        # Multiple categories
        raw_cats_multi = ["Occupational therapy equipment", "Wheelchairs", "Supports & Braces"]
        mapped_multi = set(resolve_category_slugs(99999, raw_cats_multi))
        expected = {"rehabilitation-equipment", "mobility-aids", "orthopedic-supports"}
        self.assertEqual(mapped_multi, expected)

    def test_special_uncategorized_product_overrides(self):
        """Verify product-specific category overrides for previously uncategorized items."""
        self.assertEqual(resolve_category_slugs(21294, ["Uncategorized"]), ["orthopedic-supports"])
        self.assertEqual(resolve_category_slugs(21322, ["Uncategorized"]), ["rehabilitation-equipment"])
        self.assertEqual(resolve_category_slugs(21331, ["Uncategorized"]), ["orthopedic-supports"])
        self.assertEqual(resolve_category_slugs(21362, ["Uncategorized"]), ["home-care"])
        self.assertEqual(resolve_category_slugs(21375, ["Uncategorized"]), ["rehabilitation-equipment"])
        self.assertEqual(resolve_category_slugs(21401, ["Uncategorized"]), ["rehabilitation-equipment"])
        self.assertEqual(resolve_category_slugs(21407, ["Uncategorized"]), ["medical-furniture"])

    def test_special_product_21595_rehabilitation(self):
        """Product 21595 must map to Rehabilitation & Physiotherapy (rehabilitation-equipment)."""
        mapped = resolve_category_slugs(21595, [])
        self.assertEqual(mapped, ["rehabilitation-equipment"])


class WooCommerceImporterIntegrationTest(TestCase):

    def setUp(self):
        # Ensure the 5 canonical categories exist in test DB
        self.cat_mobility = Category.objects.create(name="Mobility Aids", slug="mobility-aids")
        self.cat_ortho = Category.objects.create(name="Orthopedic Supports & Braces", slug="orthopedic-supports")
        self.cat_rehab = Category.objects.create(name="Rehabilitation & Physiotherapy", slug="rehabilitation-equipment")
        self.cat_furniture = Category.objects.create(name="Medical Furniture & Hospital Supplies", slug="medical-furniture")
        self.cat_home = Category.objects.create(name="Daily Living & Home Care", slug="home-care")

    def test_import_command_dry_run_and_execution_idempotency(self):
        """
        Tests end-to-end management command using small isolated test fixtures:
        - dry-run does not write to DB
        - live execution imports products, resolves multiple categories, handles 21503, skips 21590
        - second run is idempotent (no duplicate products or categories)
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            products_file = os.path.join(temp_dir, "products_fixed.tsv")
            categories_file = os.path.join(temp_dir, "categories.tsv")
            prod_cats_file = os.path.join(temp_dir, "product_categories.tsv")
            images_dir = os.path.join(temp_dir, "images")
            os.makedirs(images_dir, exist_ok=True)

            # 1. Write categories.tsv
            with open(categories_file, 'w', encoding='utf-8') as f:
                f.write("category_id\tname\tslug\n")
                f.write("101\tSupports & Braces\tsupports-braces\n")
                f.write("102\tWheelchairs\twheelchairs\n")

            # 2. Write product_categories.tsv
            with open(prod_cats_file, 'w', encoding='utf-8') as f:
                f.write("product_id\tcategory_id\n")
                f.write("21100\t101\n")
                f.write("21100\t102\n")  # Multiple categories for 21100

            # 3. Write products_fixed.tsv
            with open(products_file, 'w', encoding='utf-8') as f:
                headers = [
                    "id", "name", "slug", "sku", "regular_price", "sale_price",
                    "current_price", "stock_status", "stock_quantity", "manage_stock",
                    "short_description", "description"
                ]
                f.write("\t".join(headers) + "\n")
                # Record 1: Multi-category product
                f.write("21100\tFolding Wheelchair\tfolding-wheelchair\tOBC-FW-001\t15000\t13000\t13000\tinstock\t10\tyes\tShort info\t<p>Full description</p>\n")
                # Record 2: Exception 21503 (empty name, price 10000)
                f.write("21503\tNULL\tNULL\tNULL\t10000\t9150\t10000\tinstock\t0\tno\tDigital unit\tFull description\n")
                # Record 3: Exception 21590 (no price -> skipped)
                f.write("21590\tNULL\tNULL\tNULL\tNULL\tNULL\tNULL\tinstock\t0\tno\tNULL\tNULL\n")
                # Record 4: Exception 21595 (missing relationship, known category)
                f.write("21595\tInterlocking mat\tinterlocking-mat\tNULL\t2500\tNULL\t2500\tinstock\t5\tyes\tMat\tFull mat description\n")

            # -------------------------------------------------------------
            # STEP A: Dry Run
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir,
                dry_run=True,
                skip_images=True
            )
            # Verify no products were created in DB during dry-run
            self.assertEqual(Product.objects.filter(woocommerce_id__in=[21100, 21503, 21590, 21595]).count(), 0)

            # -------------------------------------------------------------
            # STEP B: Live Import
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir,
                skip_images=True
            )

            # Verify Product 21100
            prod_21100 = Product.objects.get(woocommerce_id=21100)
            self.assertEqual(prod_21100.name, "Folding Wheelchair")
            self.assertEqual(prod_21100.sku, "OBC-FW-001")
            self.assertEqual(prod_21100.price, Decimal("13000.00"))
            self.assertEqual(prod_21100.compare_at_price, Decimal("15000.00"))
            self.assertTrue(prod_21100.is_on_sale)
            self.assertTrue(prod_21100.stock_managed)
            self.assertEqual(prod_21100.stock_quantity, 10)
            # Verify multiple categories assigned to 21100
            cat_slugs_21100 = set(prod_21100.categories.values_list('slug', flat=True))
            self.assertEqual(cat_slugs_21100, {"orthopedic-supports", "mobility-aids"})

            # Verify Product 21503 (corrected name, not on sale)
            prod_21503 = Product.objects.get(woocommerce_id=21503)
            self.assertEqual(prod_21503.name, "TENS Unit 7000 Digital Machine")
            self.assertEqual(prod_21503.price, Decimal("10000.00"))
            self.assertIsNone(prod_21503.compare_at_price)
            self.assertFalse(prod_21503.is_on_sale)
            self.assertIsNone(prod_21503.sku)

            # Verify Product 21590 was skipped (missing price)
            self.assertFalse(Product.objects.filter(woocommerce_id=21590).exists())

            # Verify Product 21595 (Rehabilitation & Physiotherapy)
            prod_21595 = Product.objects.get(woocommerce_id=21595)
            self.assertEqual(prod_21595.name, "Interlocking mat")
            self.assertEqual(list(prod_21595.categories.values_list('slug', flat=True)), ["rehabilitation-equipment"])

            initial_count = Product.objects.count()

            # -------------------------------------------------------------
            # STEP C: Idempotency (Second Run Without --update)
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir,
                skip_images=True
            )
            # Total products in database must NOT change
            self.assertEqual(Product.objects.count(), initial_count)

            # -------------------------------------------------------------
            # STEP D: Idempotency (Third Run With --update)
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir,
                skip_images=True,
                update=True
            )
            self.assertEqual(Product.objects.count(), initial_count)
