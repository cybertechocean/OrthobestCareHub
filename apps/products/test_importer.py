import os
import tempfile
from decimal import Decimal
from urllib.parse import unquote
from django.test import TestCase
from django.core.management import call_command
from apps.products.models import Product, Category, ProductImage
from apps.products.management.commands.import_woocommerce import (
    clean_val,
    parse_price,
    resolve_price,
    resolve_stock,
    resolve_category_slugs,
    find_physical_image,
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

    def test_requirement_a_occupational_therapy(self):
        """A normal product with Occupational therapy equipment receives Rehabilitation & Physiotherapy."""
        mapped = resolve_category_slugs(99001, ["Occupational therapy equipment"])
        self.assertEqual(mapped, ["rehabilitation-equipment"])

    def test_requirement_b_multiple_categories(self):
        """A product with multiple WooCommerce categories receives multiple unique Django categories."""
        raw_cats = ["Occupational therapy equipment", "Wheelchairs"]
        mapped = set(resolve_category_slugs(99002, raw_cats))
        self.assertEqual(mapped, {"rehabilitation-equipment", "mobility-aids"})

    def test_requirement_c_deduplication(self):
        """Multiple WooCommerce categories mapping to the same Django category map only once."""
        raw_cats = ["Orthopaedic Appliances", "Supports & Braces"]
        mapped = resolve_category_slugs(99003, raw_cats)
        self.assertEqual(mapped, ["orthopedic-supports"])

    def test_requirement_d_html_entity_unescaping(self):
        """HTML entities like Supports &amp; Braces resolve cleanly to orthopedic-supports."""
        self.assertEqual(resolve_category_slugs(99004, ["Supports &amp; Braces"]), ["orthopedic-supports"])
        self.assertEqual(resolve_category_slugs(99005, ["Hospital Beds &amp; Furniture"]), ["medical-furniture"])
        self.assertEqual(resolve_category_slugs(99006, ["Fitness &amp; Exercise Equipment"]), ["rehabilitation-equipment"])

    def test_requirement_g_recursive_image_discovery(self):
        """Verify recursive image discovery finds files inside year/month subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            images_dir = os.path.join(temp_dir, "images")
            sub1 = os.path.join(images_dir, "2026", "01")
            sub2 = os.path.join(images_dir, "2026", "02")
            sub3 = os.path.join(images_dir, "2026", "07")
            os.makedirs(sub1, exist_ok=True)
            os.makedirs(sub2, exist_ok=True)
            os.makedirs(sub3, exist_ok=True)

            img1_path = os.path.join(sub1, "wheelchair-pro.jpg")
            img2_path = os.path.join(sub2, "mat%20exercise.png")
            img3_path = os.path.join(sub3, "brace.jpg")
            with open(img1_path, 'w') as f:
                f.write("img1")
            with open(img2_path, 'w') as f:
                f.write("img2")
            with open(img3_path, 'w') as f:
                f.write("img3")

            # Index images recursively as import_woocommerce does
            disk_images = {}
            for root, dirs, files in os.walk(images_dir):
                for f in files:
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, images_dir).replace('\\', '/')
                    disk_images[rel_path] = full_path
                    disk_images[rel_path.lower()] = full_path
                    disk_images[unquote(rel_path).lower()] = full_path
                    fn = os.path.basename(f)
                    disk_images[fn.lower()] = full_path
                    disk_images[unquote(fn).lower()] = full_path

            # Test lookup by relative path and by basename
            self.assertEqual(find_physical_image("2026/01/wheelchair-pro.jpg", disk_images), img1_path)
            self.assertEqual(find_physical_image("wheelchair-pro.jpg", disk_images), img1_path)
            self.assertEqual(find_physical_image("mat exercise.png", disk_images), img2_path)
            self.assertEqual(find_physical_image("brace.jpg", disk_images), img3_path)


class WooCommerceImporterIntegrationTest(TestCase):

    def setUp(self):
        self.cat_mobility = Category.objects.create(name="Mobility Aids", slug="mobility-aids")
        self.cat_ortho = Category.objects.create(name="Orthopedic Supports & Braces", slug="orthopedic-supports")
        self.cat_rehab = Category.objects.create(name="Rehabilitation & Physiotherapy", slug="rehabilitation-equipment")
        self.cat_furniture = Category.objects.create(name="Medical Furniture & Hospital Supplies", slug="medical-furniture")
        self.cat_home = Category.objects.create(name="Daily Living & Home Care", slug="home-care")

    def test_full_catalog_import_flow(self):
        """
        Tests:
        - Requirement E: Product 21085 resolves to Mobility Aids, Rehabilitation & Physiotherapy, Orthopedic Supports
        - Requirement F: Product 21595 resolves to Rehabilitation & Physiotherapy even with missing price
        - Requirement H: Image attachments resolve to physical files in year/month subdirectories
        - Requirement I: Dry-run performs no database or filesystem writes
        - Requirement J: Idempotency remains intact across multiple runs
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            products_file = os.path.join(temp_dir, "products_fixed.tsv")
            categories_file = os.path.join(temp_dir, "categories.tsv")
            prod_cats_file = os.path.join(temp_dir, "product_categories.tsv")
            attachments_file = os.path.join(temp_dir, "attachments.tsv")
            prod_imgs_file = os.path.join(temp_dir, "product_images.tsv")
            prod_atts_file = os.path.join(temp_dir, "product_attachments.tsv")

            # Setup nested images directory
            images_sub = os.path.join(temp_dir, "images", "2026", "03")
            os.makedirs(images_sub, exist_ok=True)
            wheelchair_img = os.path.join(images_sub, "wheelchair-21085.jpg")
            with open(wheelchair_img, 'wb') as f:
                f.write(b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00')  # minimal dummy JPEG header

            # 1. categories.tsv using term_taxonomy_id / term_id headers
            with open(categories_file, 'w', encoding='utf-8') as f:
                f.write("term_taxonomy_id\tterm_id\tname\tslug\n")
                f.write("1\t10\tWheelchairs\twheelchairs\n")
                f.write("2\t20\tOccupational therapy equipment\toccupational-therapy-equipment\n")
                f.write("3\t30\tSupports &amp; Braces\tsupports-braces\n")

            # 2. product_categories.tsv using object_id / term_taxonomy_id headers
            with open(prod_cats_file, 'w', encoding='utf-8') as f:
                f.write("object_id\tterm_taxonomy_id\n")
                # Product 21085 attached to all 3 categories
                f.write("21085\t1\n")
                f.write("21085\t2\n")
                f.write("21085\t3\n")
                # Product 21595 attached to Occupational therapy equipment
                f.write("21595\t2\n")

            # 3. attachments.tsv
            with open(attachments_file, 'w', encoding='utf-8') as f:
                f.write("attachment_id\tpath\n")
                f.write("5001\t2026/03/wheelchair-21085.jpg\n")

            # 4. product_images.tsv
            with open(prod_imgs_file, 'w', encoding='utf-8') as f:
                f.write("product_id\tthumbnail_id\n")
                f.write("21085\t5001\n")

            # 5. product_attachments.tsv
            with open(prod_atts_file, 'w', encoding='utf-8') as f:
                f.write("product_id\tattachment_id\n")
                f.write("21085\t5001\n")

            # 6. products_fixed.tsv
            with open(products_file, 'w', encoding='utf-8') as f:
                headers = [
                    "id", "name", "slug", "sku", "regular_price", "sale_price",
                    "current_price", "stock_status", "stock_quantity", "manage_stock",
                    "short_description", "description"
                ]
                f.write("\t".join(headers) + "\n")
                # 21085: Valid price, 3 categories, 1 image
                f.write("21085\tStandard wheelchair\tstandard-wheelchair\tOBC-WC-21085\t14000\t12000\t12000\tinstock\t8\tyes\tDurable wheelchair\t<p>Full description</p>\n")
                # 21590: No price -> skipped
                f.write("21590\tNULL\tNULL\tNULL\tNULL\tNULL\tNULL\tinstock\t0\tno\tNULL\tNULL\n")
                # 21595: Interlocking mat, NO price -> must be skipped, but category verified
                f.write("21595\tInterlocking mat\tinterlocking-mat\tNULL\tNULL\tNULL\tNULL\tinstock\t5\tyes\tMat\tFull mat description\n")
                # 21503: Empty name, price 10000 -> name set to TENS Unit 7000 Digital Machine
                f.write("21503\tNULL\tNULL\tNULL\t10000\t9150\t10000\tinstock\t0\tno\tDigital unit\tFull description\n")

            # -------------------------------------------------------------
            # STEP I: Dry Run (No DB or filesystem writes)
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir,
                dry_run=True
            )
            # No products or images created in DB
            self.assertEqual(Product.objects.filter(woocommerce_id__in=[21085, 21590, 21595, 21503]).count(), 0)
            self.assertEqual(ProductImage.objects.count(), 0)

            # -------------------------------------------------------------
            # LIVE IMPORT
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir
            )

            # Requirement E: Verify Product 21085 has all 3 unique Django categories
            prod_21085 = Product.objects.get(woocommerce_id=21085)
            self.assertEqual(prod_21085.name, "Standard wheelchair")
            cats_21085 = set(prod_21085.categories.values_list('slug', flat=True))
            expected_cats_21085 = {"mobility-aids", "rehabilitation-equipment", "orthopedic-supports"}
            self.assertEqual(cats_21085, expected_cats_21085)

            # Requirement H: Image attachment resolved to physical file in 2026/03 subdirectory
            self.assertEqual(prod_21085.images.count(), 1)
            primary_img = prod_21085.primary_image
            self.assertIsNotNone(primary_img)
            self.assertTrue(primary_img.is_primary)
            self.assertIn("wheelchair-21085", primary_img.image.name)

            # Requirement F: Product 21595 was skipped because of missing price, NOT created
            self.assertFalse(Product.objects.filter(woocommerce_id=21595).exists())

            # Verify Product 21590 was skipped because of missing price
            self.assertFalse(Product.objects.filter(woocommerce_id=21590).exists())

            # Verify Product 21503 was created with corrected name and price 10000
            prod_21503 = Product.objects.get(woocommerce_id=21503)
            self.assertEqual(prod_21503.name, "TENS Unit 7000 Digital Machine")
            self.assertEqual(prod_21503.price, Decimal("10000.00"))
            self.assertFalse(prod_21503.is_on_sale)

            total_products_after_first_run = Product.objects.count()
            total_images_after_first_run = ProductImage.objects.count()

            # -------------------------------------------------------------
            # Requirement J: Idempotency (Second Run Without --update)
            # -------------------------------------------------------------
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir
            )
            self.assertEqual(Product.objects.count(), total_products_after_first_run)
            self.assertEqual(ProductImage.objects.count(), total_images_after_first_run)

            # Idempotency (Third Run With --update)
            call_command(
                'import_woocommerce',
                products_file=products_file,
                export_dir=temp_dir,
                update=True
            )
            self.assertEqual(Product.objects.count(), total_products_after_first_run)
            self.assertEqual(ProductImage.objects.count(), total_images_after_first_run)
