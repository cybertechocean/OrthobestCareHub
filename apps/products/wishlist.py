from decimal import Decimal
from .models import Product, Wishlist, WishlistItem


class WishlistService:
    """
    Hybrid Wishlist management service.
    Handles session-based wishlist for guests and database-backed wishlist for authenticated users.
    Seamlessly synchronizes guest items to database when user logs in.
    """
    SESSION_KEY = 'wishlist_product_ids'

    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        
        if self.SESSION_KEY not in self.session:
            self.session[self.SESSION_KEY] = []
        self.session_wishlist = self.session[self.SESSION_KEY]

        # If user is authenticated, ensure DB wishlist exists and merge any session items
        if self.user:
            self.db_wishlist, _ = Wishlist.objects.get_or_create(user=self.user)
            if self.session_wishlist:
                for product_id in self.session_wishlist:
                    try:
                        product = Product.objects.get(id=product_id, is_available=True)
                        WishlistItem.objects.get_or_create(wishlist=self.db_wishlist, product=product)
                    except Product.DoesNotExist:
                        continue
                self.session[self.SESSION_KEY] = []
                self.session.modified = True

    def toggle(self, product_id):
        """
        Toggles a product in the wishlist.
        Returns (in_wishlist: bool, total_count: int, product: Product)
        """
        product = Product.objects.get(id=product_id, is_available=True)
        if self.user:
            item = WishlistItem.objects.filter(wishlist=self.db_wishlist, product=product).first()
            if item:
                item.delete()
                in_wishlist = False
            else:
                WishlistItem.objects.create(wishlist=self.db_wishlist, product=product)
                in_wishlist = True
            total_count = self.db_wishlist.items.count()
        else:
            p_id = int(product_id)
            if p_id in self.session_wishlist:
                self.session_wishlist.remove(p_id)
                in_wishlist = False
            else:
                self.session_wishlist.append(p_id)
                in_wishlist = True
            self.session[self.SESSION_KEY] = self.session_wishlist
            self.session.modified = True
            total_count = len(self.session_wishlist)

        return in_wishlist, total_count, product

    def remove(self, product_id):
        """
        Removes a product from the wishlist.
        """
        try:
            product = Product.objects.get(id=product_id)
            if self.user:
                WishlistItem.objects.filter(wishlist=self.db_wishlist, product=product).delete()
            else:
                p_id = int(product_id)
                if p_id in self.session_wishlist:
                    self.session_wishlist.remove(p_id)
                    self.session[self.SESSION_KEY] = self.session_wishlist
                    self.session.modified = True
        except Product.DoesNotExist:
            pass

    def get_product_ids(self):
        """
        Returns list of product IDs currently in wishlist.
        """
        if self.user:
            return list(self.db_wishlist.items.values_list('product_id', flat=True))
        return [int(pid) for pid in self.session_wishlist]

    def get_products(self):
        """
        Returns QuerySet of Product objects in the wishlist.
        """
        ids = self.get_product_ids()
        return Product.objects.filter(id__in=ids, is_available=True).select_related('category', 'brand').prefetch_related('images')

    def count(self):
        return len(self.get_product_ids())
