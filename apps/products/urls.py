from django.urls import path
from .views import (
    ShopView, CategoryDetailView, ProductDetailView,
    ProductReviewCreateView, ProductLiveSearchApiView,
    WishlistDetailView, WishlistToggleAjaxView, WishlistRemoveView,
    WishlistMoveToCartView, ClearBrowsingHistoryView
)

app_name = 'products'

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop/category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:slug>/review/', ProductReviewCreateView.as_view(), name='add_review'),
    path('api/products/search/', ProductLiveSearchApiView.as_view(), name='live_search'),
    
    # Wishlist Endpoints
    path('wishlist/', WishlistDetailView.as_view(), name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', WishlistToggleAjaxView.as_view(), name='wishlist_toggle'),
    path('wishlist/remove/<int:product_id>/', WishlistRemoveView.as_view(), name='wishlist_remove'),
    path('wishlist/move-to-cart/<int:product_id>/', WishlistMoveToCartView.as_view(), name='wishlist_move_to_cart'),
    
    # Browsing History Endpoints
    path('history/clear/', ClearBrowsingHistoryView.as_view(), name='clear_history'),
]
