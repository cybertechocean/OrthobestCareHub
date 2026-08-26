from django.db import models
from apps.orders.models import Order


class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    transaction_id = models.CharField(max_length=150, unique=True, help_text="Reference ID / M-Pesa Receipt Number / Gateway ID")
    gateway = models.CharField(max_length=50, default="mpesa", help_text="e.g. mpesa, card, cod, manual")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="KES")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    phone_number = models.CharField(max_length=50, blank=True)
    raw_response = models.TextField(blank=True, help_text="JSON payload response received from payment provider")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['gateway', 'status']),
        ]

    def __str__(self):
        return f"Transaction {self.transaction_id} — {self.order.order_number} ({self.status})"


class MpesaPaymentLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="mpesa_logs")
    merchant_request_id = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    mpesa_receipt = models.CharField(max_length=100, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.CharField(max_length=255, blank=True)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "M-Pesa Express Log"
        verbose_name_plural = "M-Pesa Express Logs"

    def __str__(self):
        return f"M-Pesa Log #{self.checkout_request_id} for Order #{self.order.order_number}"
