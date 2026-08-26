import uuid
from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.products.models import Product

User = get_user_model()


class DeliveryZone(models.Model):
    name = models.CharField(max_length=150, help_text="e.g. Nairobi CBD & Surroundings, Kiambu & Machakos, Upcountry Courier")
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Delivery charge in KSh")
    estimated_delivery_time = models.CharField(max_length=150, default="Same Day / 24 Hours", help_text="e.g. Within 2-4 Hours, Next Day")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'delivery_fee']
        verbose_name = "Delivery Zone"
        verbose_name_plural = "Delivery Zones"

    def __str__(self):
        return f"{self.name} — KSh {self.delivery_fee:,.0f} ({self.estimated_delivery_time})"


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage Discount (%)'),
        ('fixed', 'Fixed Amount Discount (KSh)'),
    )
    code = models.CharField(max_length=50, unique=True, help_text="e.g. WELCOME10, REHAB2026")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage e.g. 10 for 10%, or fixed KSh amount")
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Minimum order subtotal to apply coupon")
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Cap on max discount amount in KSh (optional)")
    usage_limit = models.PositiveIntegerField(default=100)
    times_used = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type=='percentage' else ' KSh'})"

    def calculate_discount(self, subtotal):
        if not self.active or subtotal < self.minimum_order:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            discount = (subtotal * (self.discount_value / Decimal('100.00')))
        else:
            discount = self.discount_value

        if self.maximum_discount and discount > self.maximum_discount:
            discount = self.maximum_discount

        return min(discount, subtotal)


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing & Packing'),
        ('ready_for_dispatch', 'Ready for Dispatch'),
        ('shipped', 'Out for Delivery / In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Payment Pending'),
        ('processing', 'Processing Payment'),
        ('completed', 'Paid Successfully'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('mpesa', 'Safaricom M-Pesa (STK Push / Express)'),
        ('cash_on_delivery', 'Pay on Delivery (Cash / M-Pesa on Arrival)'),
        ('card', 'Credit / Debit Card'),
        ('manual_transfer', 'Manual M-Pesa Paybill / Bank Transfer'),
    )

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    
    # Customer Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, help_text="Kenyan phone number e.g. 0712345678 or +254712345678")
    
    # Delivery Destination in Kenya
    county = models.CharField(max_length=100, default="Nairobi")
    town_city = models.CharField(max_length=100, default="Nairobi")
    estate_address = models.CharField(max_length=255, help_text="Building, Road, Estate, House / Office Number")
    delivery_notes = models.TextField(blank=True, help_text="Special instructions for the courier/rider")
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, related_name="orders")
    
    # Financial breakdown (Stored historically at purchase time)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default="KES")
    
    coupon_code = models.CharField(max_length=50, blank=True)
    
    # Status & Payment
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='mpesa')
    payment_reference = models.CharField(max_length=100, blank=True, help_text="M-Pesa Receipt Number e.g. QKH718XXXX")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Order #{self.order_number} - {self.first_name} {self.last_name} (KSh {self.total_amount:,.0f})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            from django.utils import timezone
            year = timezone.now().year
            rand_suffix = f"{random.randint(1000, 9999)}"
            self.order_number = f"OBC-{year}-{rand_suffix}"
            while Order.objects.filter(order_number=self.order_number).exists():
                rand_suffix = f"{random.randint(1000, 9999)}"
                self.order_number = f"OBC-{year}-{rand_suffix}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'order_number': self.order_number})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    product_name = models.CharField(max_length=255, help_text="Snapshot of product name at purchase time")
    variant_name = models.CharField(max_length=150, blank=True, help_text="Snapshot of selected variant at purchase time")
    sku = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in #{self.order.order_number}"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=30)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order Status Update"
        verbose_name_plural = "Order Status Updates"

    def __str__(self):
        return f"Order #{self.order.order_number} changed to {self.status} at {self.created_at}"
