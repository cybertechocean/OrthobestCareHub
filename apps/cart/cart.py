from decimal import Decimal
from apps.products.models import Product, ProductVariant

SESSION_CART_KEY = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_CART_KEY)
        if not cart:
            cart = self.session[SESSION_CART_KEY] = {}
        self.cart = cart

    def _generate_key(self, product_id, variant_id=None):
        return f"{product_id}_{variant_id}" if variant_id else str(product_id)

    def add(self, product, variant=None, quantity=1, override_quantity=False):
        product_id = str(product.id)
        variant_id = str(variant.id) if variant else None
        item_key = self._generate_key(product_id, variant_id)

        if item_key not in self.cart:
            unit_price = float(variant.effective_price if variant else product.price)
            self.cart[item_key] = {
                'product_id': int(product_id),
                'variant_id': int(variant_id) if variant_id else None,
                'quantity': 0,
                'unit_price': unit_price,
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity

        # Stock bound check
        available_stock = variant.stock_quantity if variant else product.stock_quantity
        if self.cart[item_key]['quantity'] > available_stock:
            self.cart[item_key]['quantity'] = max(available_stock, 1)

        self.save()
        return self.cart[item_key]['quantity']

    def update_quantity(self, item_key, quantity):
        if item_key in self.cart:
            if quantity <= 0:
                self.remove(item_key)
            else:
                self.cart[item_key]['quantity'] = quantity
                self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def clear(self):
        self.session[SESSION_CART_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart, pulling live Product and ProductVariant
        data directly from the database to guarantee accurate prices & stock.
        """
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids).select_related('category').prefetch_related('images')}

        variant_ids = [item['variant_id'] for item in self.cart.values() if item['variant_id']]
        variants = {v.id: v for v in ProductVariant.objects.filter(id__in=variant_ids)} if variant_ids else {}

        for item_key, item_data in list(self.cart.items()):
            product = products.get(item_data['product_id'])
            if not product or not product.is_available:
                # Remove stale or unavailable products
                del self.cart[item_key]
                self.save()
                continue

            variant = variants.get(item_data['variant_id']) if item_data['variant_id'] else None
            price = variant.effective_price if variant else product.price
            total_item_price = price * item_data['quantity']
            
            img = product.primary_image.image.url if (product.primary_image and product.primary_image.image) else '/static/images/placeholder.jpg'

            yield {
                'key': item_key,
                'product': product,
                'variant': variant,
                'quantity': item_data['quantity'],
                'price': price,
                'total_price': total_item_price,
                'image_url': img,
            }

    def __len__(self):
        """Return total count of all items in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        """Calculate total price of all items in cart"""
        return sum(item['total_price'] for item in self)

    def is_empty(self):
        return len(self.cart) == 0
