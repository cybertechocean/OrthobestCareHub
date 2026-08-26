from django.urls import path
from .views import (
    PaymentProcessView, MpesaStkPushAjaxView,
    MpesaSimulateConfirmView, MpesaStatusCheckAjaxView, MpesaCallbackView
)

app_name = 'payments'

urlpatterns = [
    path('payments/process/<str:order_number>/', PaymentProcessView.as_view(), name='process'),
    path('payments/mpesa/stk-push/<str:order_number>/', MpesaStkPushAjaxView.as_view(), name='mpesa_stk_push'),
    path('payments/mpesa/simulate-confirm/<str:checkout_request_id>/', MpesaSimulateConfirmView.as_view(), name='mpesa_simulate_confirm'),
    path('payments/mpesa/status-check/<str:order_number>/', MpesaStatusCheckAjaxView.as_view(), name='mpesa_status_check'),
    path('payments/mpesa/callback/', MpesaCallbackView.as_view(), name='mpesa_callback'),
]
