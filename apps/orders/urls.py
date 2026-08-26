from django.urls import path
from .views import (
    CheckoutView, CouponValidateAjaxView, OrderConfirmationView,
    OrderTrackingView, OrderDetailView
)

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/coupon/validate/', CouponValidateAjaxView.as_view(), name='coupon_validate'),
    path('order/confirmed/<str:order_number>/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('track-order/', OrderTrackingView.as_view(), name='order_track'),
    path('order/<str:order_number>/', OrderDetailView.as_view(), name='order_detail'),
]
