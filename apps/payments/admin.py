from django.contrib import admin
from .models import PaymentTransaction, MpesaPaymentLog

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'gateway', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('gateway', 'status', 'created_at')
    search_fields = ('transaction_id', 'order__order_number', 'phone_number')
    readonly_fields = ('transaction_id', 'order', 'gateway', 'amount', 'currency', 'status', 'phone_number', 'raw_response', 'created_at')


@admin.register(MpesaPaymentLog)
class MpesaPaymentLogAdmin(admin.ModelAdmin):
    list_display = ('checkout_request_id', 'order', 'phone_number', 'amount', 'mpesa_receipt', 'is_successful', 'created_at')
    list_filter = ('is_successful', 'created_at')
    search_fields = ('checkout_request_id', 'merchant_request_id', 'mpesa_receipt', 'phone_number', 'order__order_number')
    readonly_fields = ('order', 'merchant_request_id', 'checkout_request_id', 'phone_number', 'amount', 'mpesa_receipt', 'result_code', 'result_desc', 'is_successful', 'created_at', 'updated_at')
