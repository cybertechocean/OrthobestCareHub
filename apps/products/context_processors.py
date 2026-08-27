from .wishlist import WishlistService


def wishlist_context(request):
    """
    Exposes wishlist_total_count and wishlist_product_ids globally to all templates.
    """
    wishlist = WishlistService(request)
    return {
        'wishlist_total_count': wishlist.count(),
        'wishlist_product_ids': wishlist.get_product_ids(),
    }
