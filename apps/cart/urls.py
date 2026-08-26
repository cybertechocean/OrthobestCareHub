from django.urls import path
from .views import CartDetailView, CartAddView, CartUpdateView, CartRemoveView, CartClearView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('cart/update/<str:item_key>/', CartUpdateView.as_view(), name='cart_update'),
    path('cart/remove/<str:item_key>/', CartRemoveView.as_view(), name='cart_remove'),
    path('cart/clear/', CartClearView.as_view(), name='cart_clear'),
]
