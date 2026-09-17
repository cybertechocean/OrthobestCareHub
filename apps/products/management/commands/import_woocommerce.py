import os
import re
import csv
import html
import collections
from decimal import Decimal, InvalidOperation
from urllib.parse import unquote

from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
from django.utils.text import slugify
from django.utils.html import strip_tags

from apps.products.models import Product, Category, ProductImage

# Default paths for production server
DEFAULT_PRODUCTS_FILE = "/home2/genzcons/products_fixed.tsv"
DEFAULT_EXPORT_DIR = "/home2/genzcons/woocommerce_export"

# Category Mapping from WooCommerce category names to Django Category slugs
WOOCOMMERCE_CATEGORY_MAP = {
    # Orthopedic Supports & Braces
    "orthopaedic appliances": "orthopedic-supports",
    "orthopaedic appliance": "orthopedic-supports",
    "orthopedic appliances": "orthopedic-supports",
    "orthopedic appliance": "orthopedic-supports",
    "supports & braces": "orthopedic-supports",
    "supports and braces": "orthopedic-supports",
    "supports": "orthopedic-supports",
    "braces": "orthopedic-supports",
    
    # Rehabilitation & Physiotherapy
    "physiotherapy products": "rehabilitation-equipment",
    "physiotherapy product": "rehabilitation-equipment",
    "physiotherapy": "rehabilitation-equipment",
    "occupational therapy equipment": "rehabilitation-equipment",
    "occupational therapy": "rehabilitation-equipment",
    "fitness & exercise equipment": "rehabilitation-equipment",
    "fitness and exercise equipment": "rehabilitation-equipment",
    
    # Daily Living & Home Care
    "speech therapy appliances": "home-care",
    "speech therapy appliance": "home-care",
    "speech therapy": "home-care",
    
    # Mobility Aids
    "mobility aids": "mobility-aids",
    "mobility aid": "mobility-aids",
    "mobility": "mobility-aids",
    "wheelchairs": "mobility-aids",
    "wheelchair": "mobility-aids",
    
    # Medical Furniture & Hospital Supplies
    "hospital beds & furniture": "medical-furniture",
    "hospital beds and furniture": "medical-furniture",
    "hospital beds": "medical-furniture",
    "icu solutions and machines": "medical-furniture",
    "icu solutions": "medical-furniture",
    "laboratory equipment": "medical-furniture",
    "general medical": "medical-furniture",
}

# Slug equivalents
WOOCOMMERCE_CATEGORY_SLUG_MAP = {
    "orthopaedic-appliances": "orthopedic-supports",
    "orthopedic-appliances": "orthopedic-supports",
    "supports-braces": "orthopedic-supports",
    "supports-and-braces": "orthopedic-supports",
    "physiotherapy-products": "rehabilitation-equipment",
    "physiotherapy": "rehabilitation-equipment",
    "occupational-therapy-equipment": "rehabilitation-equipment",
    "occupational-therapy": "rehabilitation-equipment",
    "speech-therapy-appliances": "home-care",
    "speech-therapy": "home-care",
    "mobility-aids": "mobility-aids",
    "wheelchairs": "mobility-aids",
    "wheelchair": "mobility-aids",
    "hospital-beds-furniture": "medical-furniture",
    "hospital-beds-and-furniture": "medical-furniture",
    "icu-solutions-and-machines": "medical-furniture",
    "laboratory-equipment": "medical-furniture",
    "fitness-exercise-equipment": "rehabilitation-equipment",
    "fitness-and-exercise-equipment": "rehabilitation-equipment",
    "general-medical": "medical-furniture",
    # Django slug self-mappings
    "orthopedic-supports": "orthopedic-supports",
    "rehabilitation-equipment": "rehabilitation-equipment",
    "home-care": "home-care",
    "medical-furniture": "medical-furniture",
}

# Product-specific category overrides (e.g. Uncategorized products & special cases)
PRODUCT_SPECIFIC_CATEGORIES = {
    21294: ["orthopedic-supports"],        # Compression Stockings Thigh Length (Dyna)
    21322: ["rehabilitation-equipment"],   # Infrared Heating Lamp Desktop
    21331: ["orthopedic-supports"],        # Black Thigh High Compression Stockings
    21362: ["home-care"],                  # 6 in 1 Montensori bead game
    21375: ["rehabilitation-equipment"],   # Therapy Wedge
    21401: ["rehabilitation-equipment"],   # Generic Thera Band Set of 5
    21407: ["medical-furniture"],          # Manual Patient Transfer
    21595: ["rehabilitation-equipment"],   # Interlocking mat (both source categories map to Rehabilitation & Physiotherapy)
}


def clean_val(val):
    """
    Strips whitespace and converts literal 'NULL' (case-insensitive) or empty strings to None.
    """
    if val is None:
        return None
    val = str(val).strip()
    if val.upper() == 'NULL' or val == '':
        return None
    return val


def extract_field(row, candidate_names, default=None):
    """
    Looks for candidate names (case-insensitive) in a row dictionary.
    Returns cleaned value or default.
    """
    row_lower = {k.lower().strip(): v for k, v in row.items() if k is not None}
    for name in candidate_names:
        name_lower = name.lower().strip()
        if name_lower in row_lower:
            val = clean_val(row_lower[name_lower])
            if val is not None:
                return val
    # Fallback to substring matching on keys
    for k_lower, v in row_lower.items():
        for name in candidate_names:
            name_lower = name.lower().strip()
            if name_lower == k_lower or f"_{name_lower}" in k_lower or f"{name_lower}_" in k_lower:
                val = clean_val(v)
                if val is not None:
                    return val
    return default


def parse_price(val):
    """
    Parses a Decimal price from string, stripping currency and commas.
    Returns None if missing or invalid.
    """
    cleaned = clean_val(val)
    if cleaned is None:
        return None
    cleaned = cleaned.replace(',', '').replace('KSh', '').replace('KES', '').strip()
    try:
        price = Decimal(cleaned)
        if price < 0:
            return None
        return price
    except (InvalidOperation, ValueError):
        return None


def resolve_price(current_price_raw, regular_price_raw, sale_price_raw, wc_id=None):
    """
    Determines selling price and compare_at_price according to business rules:
    - Primary price: current_price -> regular_price -> sale_price.
    - compare_at_price only set if regular_price > selling_price.
    - Special rule for 21503: price = 10000, compare_at_price = None (not on sale).
    Returns (selling_price, compare_at_price, is_on_sale).
    """
    current_price = parse_price(current_price_raw)
    regular_price = parse_price(regular_price_raw)
    sale_price = parse_price(sale_price_raw)

    if wc_id == 21503:
        return Decimal("10000.00"), None, False

    selling_price = None
    if current_price is not None:
        selling_price = current_price
    elif regular_price is not None:
        selling_price = regular_price
    elif sale_price is not None:
        selling_price = sale_price
    else:
        return None, None, False

    compare_at_price = None
    if regular_price is not None and regular_price > selling_price:
        compare_at_price = regular_price

    is_on_sale = bool(compare_at_price and compare_at_price > selling_price)
    return selling_price, compare_at_price, is_on_sale


def resolve_stock(manage_stock_raw, stock_status_raw, stock_qty_raw):
    """
    Maps stock status and stock quantity:
    - stock_status: 'instock' -> True, 'outofstock' -> False
    - manage_stock: 'yes'/'true'/'1' -> stock_managed = True
    - if not actively managed: stock_managed = False, stock_quantity = 0
    Returns (stock_managed, stock_quantity, is_available).
    """
    manage_stock_clean = clean_val(manage_stock_raw)
    stock_status_clean = clean_val(stock_status_raw)
    stock_qty_clean = clean_val(stock_qty_raw)

    parsed_qty = None
    if stock_qty_clean is not None:
        try:
            parsed_qty = int(float(stock_qty_clean))
        except (ValueError, TypeError):
            parsed_qty = None

    if manage_stock_clean and manage_stock_clean.lower() in ('yes', 'true', '1'):
        stock_managed = True
        stock_quantity = parsed_qty if (parsed_qty is not None and parsed_qty >= 0) else 0
    elif manage_stock_clean and manage_stock_clean.lower() in ('no', 'false', '0'):
        stock_managed = False
        stock_quantity = parsed_qty if (parsed_qty is not None and parsed_qty >= 0) else 0
    elif parsed_qty is not None and parsed_qty > 0:
        stock_managed = True
        stock_quantity = parsed_qty
    else:
        stock_managed = False
        stock_quantity = 0

    if stock_status_clean:
        status_norm = stock_status_clean.lower().replace('-', '').replace('_', '').replace(' ', '')
        if 'outofstock' in status_norm:
            is_available = False
        elif 'instock' in status_norm:
            is_available = True
        else:
            is_available = True
    else:
        is_available = (stock_quantity > 0) if stock_managed else True

    return stock_managed, stock_quantity, is_available


def load_tsv_rows(filepath):
    """
    Loads TSV rows as a list of dicts with cleaned values.
    Supports utf-8, utf-8-sig, and latin-1 fallback encodings.
    """
    if not os.path.exists(filepath):
        return []

    for enc in ('utf-8', 'utf-8-sig', 'latin-1', 'cp1252'):
        try:
            with open(filepath, 'r', encoding=enc) as f:
                reader = csv.DictReader(f, delimiter='\t')
                rows = []
                for row in reader:
                    cleaned_row = {
                        k.strip(): clean_val(v)
                        for k, v in row.items() if k is not None
                    }
                    rows.append(cleaned_row)
                return rows
        except UnicodeDecodeError:
            continue
    return []


def resolve_category_slugs(wc_id, raw_categories_list):
    """
    Maps a list of raw WooCommerce category names/slugs to unique Django category slugs.
    Normalizes HTML entities (e.g. Supports &amp; Braces -> Supports & Braces).
    Handles known product overrides and deduplication.
    """
    target_slugs = set()

    # 1. Product-specific category overrides
    if wc_id in PRODUCT_SPECIFIC_CATEGORIES:
        for slug in PRODUCT_SPECIFIC_CATEGORIES[wc_id]:
            target_slugs.add(slug)

    for cat_item in raw_categories_list:
        if not cat_item:
            continue

        # Unescape HTML entities e.g. &amp; -> &
        unescaped = html.unescape(str(cat_item))
        # Split by comma or pipe if multiple categories in string
        parts = re.split(r'[,|]', unescaped)
        for part in parts:
            part_str = re.sub(r'\s+', ' ', part).strip()
            if not part_str:
                continue
            part_lower = part_str.lower()
            
            # Skip Uncategorized
            if part_lower in ('uncategorized', 'uncategorised'):
                continue

            # Check exact category map
            if part_lower in WOOCOMMERCE_CATEGORY_MAP:
                target_slugs.add(WOOCOMMERCE_CATEGORY_MAP[part_lower])
                continue

            # Check slug map
            part_slug = slugify(part_str)
            if part_slug in WOOCOMMERCE_CATEGORY_SLUG_MAP:
                target_slugs.add(WOOCOMMERCE_CATEGORY_SLUG_MAP[part_slug])
                continue

            # Check partial / substring match on keys
            matched = False
            for map_key, django_slug in WOOCOMMERCE_CATEGORY_MAP.items():
                if map_key == part_lower or map_key in part_lower or part_lower in map_key:
                    target_slugs.add(django_slug)
                    matched = True
                    break

    return list(target_slugs)


def find_physical_image(raw_path, disk_images):
    """
    Locates an image's actual physical file path using indexed disk images.
    Handles subdirectories (e.g. 2026/01/img.jpg), URL paths, and URL encoding.
    """
    if not raw_path:
        return None

    clean_path = raw_path.split('?')[0].replace('\\', '/')
    if '/uploads/' in clean_path:
        clean_path = clean_path.split('/uploads/', 1)[1]
    clean_path = clean_path.lstrip('/')

    candidates = [
        clean_path,
        clean_path.lower(),
        unquote(clean_path).lower(),
        os.path.basename(clean_path),
        os.path.basename(clean_path).lower(),
        unquote(os.path.basename(clean_path)).lower(),
    ]
    for cand in candidates:
        if cand in disk_images and os.path.isfile(disk_images[cand]):
            return disk_images[cand]
    return None


class Command(BaseCommand):
    help = "Imports WooCommerce products, categories, stock, and images into Orthobest Care Hub Django application"

    def add_arguments(self, parser):
        parser.add_argument(
            '--products-file',
            type=str,
            default=DEFAULT_PRODUCTS_FILE,
            help=f"Path to products_fixed.tsv (Default: {DEFAULT_PRODUCTS_FILE})"
        )
        parser.add_argument(
            '--export-dir',
            type=str,
            default=DEFAULT_EXPORT_DIR,
            help=f"Path to woocommerce_export directory containing TSVs and images (Default: {DEFAULT_EXPORT_DIR})"
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Simulate import without modifying database or media storage"
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help="Skip importing product images"
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help="Update existing products matching woocommerce_id instead of skipping them"
        )

    def handle(self, *args, **options):
        products_file = options['products_file']
        export_dir = options['export_dir']
        dry_run = options['dry_run']
        skip_images = options['skip_images']
        update_existing = options['update']

        self.stdout.write(self.style.NOTICE("=" * 60))
        self.stdout.write(self.style.NOTICE("Orthobest Care Hub — WooCommerce Catalog Importer"))
        self.stdout.write(self.style.NOTICE("=" * 60))
        self.stdout.write(f"Products File: {products_file}")
        self.stdout.write(f"Export Dir:    {export_dir}")
        self.stdout.write(f"Mode:          {'DRY RUN (No database/file writes)' if dry_run else 'LIVE IMPORT'}")
        self.stdout.write(f"Skip Images:   {skip_images}")
        self.stdout.write(f"Update Existing: {update_existing}")
        self.stdout.write(self.style.NOTICE("-" * 60))

        if not os.path.exists(products_file):
            self.stderr.write(self.style.ERROR(f"Error: Products file not found at: {products_file}"))
            return

        # 1. Load Existing Django Categories
        category_cache = {c.slug: c for c in Category.objects.all()}
        self.stdout.write(f"Loaded {len(category_cache)} existing Django categories:")
        for c in category_cache.values():
            self.stdout.write(f"  • {c.name} ({c.slug})")

        # 2. Load WooCommerce Auxiliary Export Files
        categories_tsv_path = os.path.join(export_dir, 'categories.tsv')
        product_categories_tsv_path = os.path.join(export_dir, 'product_categories.tsv')
        product_images_tsv_path = os.path.join(export_dir, 'product_images.tsv')
        product_attachments_tsv_path = os.path.join(export_dir, 'product_attachments.tsv')
        attachments_tsv_path = os.path.join(export_dir, 'attachments.tsv')
        images_dir = os.path.join(export_dir, 'images')

        # Load categories.tsv
        wc_categories = {}
        category_rows = load_tsv_rows(categories_tsv_path)
        for row in category_rows:
            cat_id = extract_field(row, ['category_id', 'term_taxonomy_id', 'term_id', 'cat_id', 'cat_ID', 'id', 'ID'])
            cat_name_raw = extract_field(row, ['name', 'category_name', 'cat_name', 'term_name', 'title'])
            cat_slug_raw = extract_field(row, ['slug', 'category_slug', 'cat_slug', 'term_slug', 'category_nicename', 'nicename'])
            
            # If no named column matched, check if column 0 is an integer
            if not cat_id and row:
                first_val = list(row.values())[0]
                if first_val and str(first_val).isdigit():
                    cat_id = str(first_val)

            if cat_name_raw:
                cat_name = html.unescape(cat_name_raw)
                cat_name = re.sub(r'\s+', ' ', cat_name).strip()
            else:
                cat_name = ''

            if cat_slug_raw:
                cat_slug = cat_slug_raw.strip().lower()
            else:
                cat_slug = slugify(cat_name)

            cat_info = {
                'name': cat_name,
                'slug': cat_slug,
            }

            # Index under all candidate IDs in the row to guarantee relationship matches
            for id_col in ('category_id', 'term_taxonomy_id', 'term_id', 'cat_id', 'cat_ID', 'id', 'ID'):
                val = extract_field(row, [id_col])
                if val:
                    wc_categories[str(val)] = cat_info
            if cat_id:
                wc_categories[str(cat_id)] = cat_info
            if cat_name:
                wc_categories[cat_name.lower()] = cat_info
            if cat_slug:
                wc_categories[cat_slug.lower()] = cat_info

        self.stdout.write(f"Loaded {len(category_rows)} categories from {categories_tsv_path} (indexed {len(wc_categories)} lookup keys)")

        # Load product_categories.tsv
        product_wc_categories = collections.defaultdict(list)
        prod_cat_rows = load_tsv_rows(product_categories_tsv_path)
        for row in prod_cat_rows:
            # Match product ID
            prod_id = extract_field(row, ['object_id', 'product_id', 'post_id', 'prod_id', 'id', 'ID'])
            # Match category identifier (term_taxonomy_id, term_id, category_id, etc.)
            cat_ref = extract_field(row, ['term_taxonomy_id', 'term_id', 'category_id', 'cat_id', 'cat_ID', 'term', 'category', 'taxonomy_id'])

            # Fallback if unnamed or unknown headers
            if (not prod_id or not cat_ref) and len(row) >= 2:
                vals = list(row.values())
                if not prod_id and vals[0] and str(vals[0]).isdigit():
                    prod_id = str(vals[0])
                if not cat_ref and vals[1]:
                    cat_ref = str(vals[1])

            if prod_id and cat_ref:
                cat_ref_str = str(cat_ref).strip()
                cat_info = wc_categories.get(cat_ref_str) or wc_categories.get(cat_ref_str.lower())
                if cat_info:
                    product_wc_categories[str(prod_id)].append(cat_info['name'])
                    product_wc_categories[str(prod_id)].append(cat_info['slug'])
                else:
                    # Direct category string fallback
                    product_wc_categories[str(prod_id)].append(cat_ref_str)

        self.stdout.write(f"Loaded {len(prod_cat_rows)} product-category relationships for {len(product_wc_categories)} products")

        # Load attachments.tsv
        attachment_files = {}
        att_rows = load_tsv_rows(attachments_tsv_path)
        for row in att_rows:
            att_id = extract_field(row, ['attachment_id', 'post_id', 'id', 'ID'])
            raw_path = extract_field(row, ['filename', 'file_name', 'file', 'path', '_wp_attached_file', 'guid', 'url', 'post_title'])
            if att_id and raw_path:
                attachment_files[str(att_id)] = raw_path

        self.stdout.write(f"Loaded {len(attachment_files)} attachment records from {attachments_tsv_path}")

        # Load product_images.tsv and product_attachments.tsv
        product_images_map = collections.defaultdict(list)
        p_img_rows = load_tsv_rows(product_images_tsv_path)
        for row in p_img_rows:
            prod_id = extract_field(row, ['object_id', 'product_id', 'post_id', 'prod_id', 'id', 'ID'])
            img_ref = extract_field(row, ['thumbnail_id', '_thumbnail_id', 'image_id', 'attachment_id', 'id', 'ID', 'filename', 'file'])
            is_thumb = extract_field(row, ['is_thumbnail', 'is_featured', 'is_primary', 'thumbnail'])
            order_val = extract_field(row, ['menu_order', 'order', 'position', 'display_order'])

            if prod_id and img_ref:
                img_path = attachment_files.get(str(img_ref), str(img_ref))
                is_p = True  # In product_images.tsv, records typically denote featured/primary image
                if is_thumb is not None:
                    is_p = str(is_thumb).lower() in ('1', 'true', 'yes', 'thumbnail', 'featured')
                int_order = 0
                if order_val is not None:
                    try:
                        int_order = int(order_val)
                    except ValueError:
                        int_order = 0
                product_images_map[str(prod_id)].append({
                    'filename': img_path,
                    'is_primary': is_p,
                    'order': int_order,
                    'attachment_id': str(img_ref)
                })

        p_att_rows = load_tsv_rows(product_attachments_tsv_path)
        for row in p_att_rows:
            prod_id = extract_field(row, ['object_id', 'product_id', 'post_id', 'prod_id', 'id', 'ID'])
            att_id = extract_field(row, ['attachment_id', 'image_id', 'id', 'ID'])
            is_thumb = extract_field(row, ['is_thumbnail', 'is_featured', 'thumbnail'])
            order_val = extract_field(row, ['menu_order', 'order', 'position'])

            if prod_id and att_id:
                img_path = attachment_files.get(str(att_id), str(att_id))
                existing_att_ids = [item.get('attachment_id') for item in product_images_map[str(prod_id)]]
                if str(att_id) not in existing_att_ids:
                    is_p = False
                    if is_thumb is not None:
                        is_p = str(is_thumb).lower() in ('1', 'true', 'yes', 'thumbnail')
                    int_order = 0
                    if order_val is not None:
                        try:
                            int_order = int(order_val)
                        except ValueError:
                            int_order = 0
                    product_images_map[str(prod_id)].append({
                        'filename': img_path,
                        'is_primary': is_p,
                        'order': int_order,
                        'attachment_id': str(att_id)
                    })

        self.stdout.write(f"Loaded image relationships for {len(product_images_map)} products")

        # 3. Recursive Physical Image Discovery
        disk_images = {}
        physical_files_count = 0
        if os.path.exists(images_dir):
            for root, dirs, files in os.walk(images_dir):
                for f in files:
                    full_path = os.path.join(root, f)
                    physical_files_count += 1
                    rel_path = os.path.relpath(full_path, images_dir).replace('\\', '/')

                    # Index by relative path (e.g. 2026/01/photo.jpg)
                    disk_images[rel_path] = full_path
                    disk_images[rel_path.lower()] = full_path
                    disk_images[unquote(rel_path).lower()] = full_path

                    # Index by basename (e.g. photo.jpg)
                    fn = os.path.basename(f)
                    if fn.lower() not in disk_images:
                        disk_images[fn.lower()] = full_path
                    if unquote(fn).lower() not in disk_images:
                        disk_images[unquote(fn).lower()] = full_path

            self.stdout.write(self.style.SUCCESS(f"Recursively discovered {physical_files_count} physical image files under: {images_dir}"))
        else:
            self.stdout.write(self.style.WARNING(f"Notice: Images directory not found at: {images_dir}"))

        # 4. Read products_fixed.tsv
        product_rows = load_tsv_rows(products_file)
        self.stdout.write(f"Found {len(product_rows)} product rows in: {products_file}")
        self.stdout.write(self.style.NOTICE("-" * 60))

        # Metrics
        products_found = len(product_rows)
        products_imported = 0
        products_updated = 0
        products_skipped = 0
        products_with_missing_category = 0
        products_with_missing_images = 0
        image_references_resolved = 0
        image_references_unresolved = 0
        images_imported = 0
        images_skipped = 0
        category_relationships_created = 0
        errors_count = 0
        skipped_details = []

        for idx, row in enumerate(product_rows, start=1):
            raw_id = extract_field(row, ['id', 'ID', 'product_id', 'woocommerce_id'])
            if not raw_id:
                products_skipped += 1
                skipped_details.append({
                    'id': 'Unknown',
                    'name': 'Unknown',
                    'reason': 'missing WooCommerce ID'
                })
                continue

            try:
                wc_id = int(raw_id)
            except ValueError:
                products_skipped += 1
                skipped_details.append({
                    'id': raw_id,
                    'name': 'Unknown',
                    'reason': f'invalid WooCommerce ID ({raw_id})'
                })
                continue

            # Resolve Name
            raw_name = extract_field(row, ['name', 'post_title', 'title', 'product_name'])
            name = clean_val(raw_name)
            if wc_id == 21503:
                name = "TENS Unit 7000 Digital Machine"
            elif wc_id == 21590:
                name = "Standard Wheelchair"
            elif not name:
                name = f"WooCommerce Product {wc_id}"

            # Resolve Categories for ALL products (including special cases)
            cat_strings = list(product_wc_categories.get(str(wc_id), []))
            inline_cat = extract_field(row, ['categories', 'category'])
            if inline_cat:
                cat_strings.append(inline_cat)

            target_slugs = resolve_category_slugs(wc_id, cat_strings)
            mapped_categories = [category_cache[s] for s in target_slugs if s in category_cache]

            if not mapped_categories:
                products_with_missing_category += 1
                if wc_id != 21590:
                    self.stdout.write(self.style.WARNING(f"  Warning: No category found after mapping for WC ID {wc_id} ('{name}')"))

            # Special Product 21590 handling (must not be imported because missing price)
            if wc_id == 21590:
                products_skipped += 1
                skipped_details.append({
                    'id': 21590,
                    'name': 'Standard Wheelchair',
                    'reason': 'missing price'
                })
                self.stdout.write(f"[{idx}/{products_found}] Skipped 21590: missing price")
                continue

            # Resolve Price
            curr_p = extract_field(row, ['current_price', 'price', '_price'])
            reg_p = extract_field(row, ['regular_price', '_regular_price'])
            sale_p = extract_field(row, ['sale_price', '_sale_price'])
            selling_price, compare_at_price, is_on_sale = resolve_price(curr_p, reg_p, sale_p, wc_id=wc_id)

            if selling_price is None:
                products_skipped += 1
                skipped_details.append({
                    'id': wc_id,
                    'name': name,
                    'reason': 'missing price'
                })
                self.stdout.write(f"[{idx}/{products_found}] Skipped {wc_id}: missing price")
                continue

            # Resolve Stock & Availability
            m_stock = extract_field(row, ['manage_stock', '_manage_stock'])
            s_status = extract_field(row, ['stock_status', '_stock_status'])
            s_qty = extract_field(row, ['stock_quantity', 'stock', '_stock'])
            stock_managed, stock_quantity, is_available = resolve_stock(m_stock, s_status, s_qty)

            # Resolve SKU
            raw_sku = extract_field(row, ['sku', '_sku'])
            sku = clean_val(raw_sku)

            # Resolve Slug
            raw_slug = extract_field(row, ['slug', 'post_name'])
            clean_slug = clean_val(raw_slug)
            if clean_slug:
                base_slug = slugify(clean_slug)
            else:
                base_slug = slugify(name)
            if not base_slug:
                base_slug = f"product-{wc_id}"

            # Ensure slug uniqueness against existing products with different woocommerce_id
            target_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=target_slug).exclude(woocommerce_id=wc_id).exists():
                target_slug = f"{base_slug}-{counter}"
                counter += 1

            # Prevent duplicate non-null SKU crashes
            if sku and Product.objects.filter(sku=sku).exclude(woocommerce_id=wc_id).exists():
                self.stdout.write(self.style.WARNING(f"  Notice: SKU '{sku}' for WC ID {wc_id} already exists on another product. Setting sku=None."))
                sku = None

            # Resolve Descriptions
            raw_short_desc = extract_field(row, ['short_description', 'post_excerpt', 'excerpt'])
            raw_desc = extract_field(row, ['description', 'post_content', 'content'])
            short_desc = clean_val(raw_short_desc) or ""
            full_desc = clean_val(raw_desc) or ""

            if not short_desc:
                plain_desc = strip_tags(full_desc).strip()
                short_desc = plain_desc[:390] if plain_desc else name[:390]
            if len(short_desc) > 400:
                short_desc = short_desc[:397] + "..."
            if not full_desc:
                full_desc = name

            # Check if product already exists
            existing_product = Product.objects.filter(woocommerce_id=wc_id).first()

            if existing_product and not update_existing:
                products_skipped += 1
                skipped_details.append({
                    'id': wc_id,
                    'name': name,
                    'reason': 'already exists (use --update to update)'
                })
                self.stdout.write(f"[{idx}/{products_found}] Skipped {wc_id}: already exists")
                continue

            # Process Images list
            product_img_records = product_images_map.get(str(wc_id), [])
            if not product_img_records:
                products_with_missing_images += 1

            # Check Dry-run vs Live
            if dry_run:
                if existing_product:
                    products_updated += 1
                    action_label = "Would update"
                else:
                    products_imported += 1
                    action_label = "Would import"

                category_relationships_created += len(mapped_categories)
                cats_display = ", ".join([c.name for c in mapped_categories]) or "None"
                self.stdout.write(f"[{idx}/{products_found}] {action_label} '{name}' (WC ID: {wc_id}) | Price: KSh {selling_price:,.0f} | Stock: {stock_quantity} | Categories: {cats_display}")

                # Image resolution check in dry-run
                for img_rec in product_img_records:
                    physical_file = find_physical_image(img_rec['filename'], disk_images)
                    if physical_file:
                        image_references_resolved += 1
                        images_imported += 1
                    else:
                        image_references_unresolved += 1
                        images_skipped += 1
            else:
                try:
                    with transaction.atomic():
                        if existing_product:
                            product = existing_product
                            product.name = name
                            product.slug = target_slug
                            product.sku = sku
                            product.price = selling_price
                            product.compare_at_price = compare_at_price
                            product.short_description = short_desc
                            product.description = full_desc
                            product.stock_quantity = stock_quantity
                            product.stock_managed = stock_managed
                            product.is_available = is_available
                            product.save()
                            products_updated += 1
                            action_label = "Updated"
                        else:
                            product = Product.objects.create(
                                woocommerce_id=wc_id,
                                name=name,
                                slug=target_slug,
                                sku=sku,
                                price=selling_price,
                                compare_at_price=compare_at_price,
                                short_description=short_desc,
                                description=full_desc,
                                stock_quantity=stock_quantity,
                                stock_managed=stock_managed,
                                is_available=is_available,
                            )
                            products_imported += 1
                            action_label = "Imported"

                        # Update ManyToMany Categories
                        if mapped_categories:
                            product.categories.set(mapped_categories)
                            category_relationships_created += len(mapped_categories)

                        # Import Images
                        if not skip_images and product_img_records:
                            has_explicit_primary = any(rec['is_primary'] for rec in product_img_records)
                            sorted_img_records = sorted(product_img_records, key=lambda x: x['order'])

                            for order_idx, img_rec in enumerate(sorted_img_records):
                                is_primary = img_rec['is_primary'] if has_explicit_primary else (order_idx == 0)
                                physical_path = find_physical_image(img_rec['filename'], disk_images)

                                if not physical_path:
                                    image_references_unresolved += 1
                                    images_skipped += 1
                                    continue

                                image_references_resolved += 1
                                clean_basename = os.path.basename(physical_path)
                                clean_stem, clean_ext = os.path.splitext(clean_basename)
                                existing_img = None
                                for pi in product.images.all():
                                    pi_name = os.path.basename(pi.image.name) if pi.image else ""
                                    if pi_name == clean_basename or (clean_stem and pi_name.startswith(clean_stem) and pi_name.endswith(clean_ext)):
                                        existing_img = pi
                                        break
                                if not existing_img:
                                    existing_img = product.images.filter(display_order=order_idx).first()

                                if existing_img:
                                    if update_existing:
                                        existing_img.is_primary = is_primary
                                        existing_img.display_order = order_idx
                                        existing_img.alt_text = f"{product.name} - Orthobest Care Hub Kenya"
                                        existing_img.save()
                                    images_imported += 1
                                else:
                                    with open(physical_path, 'rb') as img_f:
                                        pi = ProductImage(
                                            product=product,
                                            is_primary=is_primary,
                                            display_order=order_idx,
                                            alt_text=f"{product.name} - Orthobest Care Hub Kenya"
                                        )
                                        pi.image.save(clean_basename, File(img_f), save=False)
                                        pi.save()
                                        images_imported += 1

                    cats_display = ", ".join([c.name for c in mapped_categories]) or "None"
                    self.stdout.write(f"[{idx}/{products_found}] {action_label} '{name}' (WC ID: {wc_id}) | Price: KSh {selling_price:,.0f} | Categories: {cats_display}")

                except Exception as e:
                    errors_count += 1
                    self.stderr.write(self.style.ERROR(f"[{idx}/{products_found}] Error importing WC ID {wc_id} ('{name}'): {e}"))

        # Print Final Summary
        self.stdout.write(self.style.NOTICE("\n" + "=" * 60))
        self.stdout.write(self.style.NOTICE("IMPORT SUMMARY"))
        self.stdout.write(self.style.NOTICE("=" * 60))
        self.stdout.write(f"Products found:                   {products_found}")
        self.stdout.write(f"Products imported / would import: {products_imported}")
        self.stdout.write(f"Products updated / would update:  {products_updated}")
        self.stdout.write(f"Products skipped:                 {products_skipped}")
        self.stdout.write(f"Products with missing category:   {products_with_missing_category}")
        self.stdout.write(f"Products with missing images:     {products_with_missing_images}")
        self.stdout.write(self.style.NOTICE("-" * 60))
        self.stdout.write(f"Physical image files discovered:  {physical_files_count}")
        self.stdout.write(f"Products with image relationships:{len(product_images_map)}")
        self.stdout.write(f"Image references resolved:        {image_references_resolved}")
        self.stdout.write(f"Image references unresolved:      {image_references_unresolved}")
        self.stdout.write(f"Images imported / stored:         {images_imported}")
        self.stdout.write(f"Images skipped / unwritten:       {images_skipped}")
        self.stdout.write(self.style.NOTICE("-" * 60))
        self.stdout.write(f"Category relationships created:   {category_relationships_created}")
        self.stdout.write(f"Errors:                           {errors_count}")
        self.stdout.write(self.style.NOTICE("=" * 60))

        if skipped_details:
            self.stdout.write(self.style.WARNING("\nSkipped Products Breakdown:"))
            for item in skipped_details:
                self.stdout.write(f"  • WC ID {item['id']}: {item['name']} (Reason: {item['reason']})")
            self.stdout.write(self.style.NOTICE("=" * 60))
