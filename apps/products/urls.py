from django.urls import path
from .views import (
    ShopView, CategoryDetailView, ProductDetailView,
    ProductReviewCreateView, ProductLiveSearchApiView
)

app_name = 'products'

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop/category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:slug>/review/', ProductReviewCreateView.as_view(), name='add_review'),
    path('api/products/search/', ProductLiveSearchApiView.as_view(), name='live_search'),
]
