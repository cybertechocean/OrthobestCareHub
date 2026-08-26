from django.contrib import admin
from django.utils.html import format_html
from .models import DeliveryZone, Coupon, Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'variant_name', 'sku', 'unit_price', 'quantity', 'total_price')
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'delivery_fee', 'estimated_delivery_time', 'display_order', 'is_active')
    list_editable = ('delivery_fee', 'estimated_delivery_time', 'display_order', 'is_active')
    list_filter = ('is_active',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'minimum_order', 'times_used', 'usage_limit', 'active')
    list_editable = ('active',)
    list_filter = ('discount_type', 'active')
    search_fields = ('code',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name_display', 'phone', 'total_formatted', 'status_badge', 'payment_status_badge', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at', 'county')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email', 'payment_reference')
    readonly_fields = ('order_number', 'subtotal', 'delivery_fee', 'discount_amount', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ("Order Meta", {
            "fields": ("order_number", "user", "created_at", "updated_at")
        }),
        ("Customer & Kenyan Contact", {
            "fields": (("first_name", "last_name"), ("phone", "email"))
        }),
        ("Delivery Destination", {
            "fields": (("county", "town_city"), "estate_address", "delivery_zone", "delivery_notes")
        }),
        ("Order & Payment Financials", {
            "fields": (("subtotal", "delivery_fee", "discount_amount"), ("total_amount", "currency"), "coupon_code")
        }),
        ("Order State & Status", {
            "fields": (("status", "payment_status"), ("payment_method", "payment_reference"))
        }),
    )

    def customer_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name_display.short_description = "Customer"

    def total_formatted(self, obj):
        return f"KSh {obj.total_amount:,.2f}"
    total_formatted.short_description = "Total"
    total_formatted.admin_order_field = "total_amount"

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'confirmed': '#3b82f6',
            'processing': '#8b5cf6',
            'ready_for_dispatch': '#06b6d4',
            'shipped': '#0ea5e9',
            'delivered': '#10b981',
            'cancelled': '#ef4444',
            'returned': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>', color, obj.get_status_display())
    status_badge.short_description = "Order Status"

    def payment_status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'processing': '#3b82f6',
            'completed': '#10b981',
            'failed': '#ef4444',
            'refunded': '#6b7280',
        }
        color = colors.get(obj.payment_status, '#6b7280')
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>', color, obj.get_payment_status_display())
    payment_status_badge.short_description = "Payment Status"
