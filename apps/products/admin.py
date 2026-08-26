from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage, ProductVariant, ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'display_order')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('name', 'sku_modifier', 'price_adjustment', 'stock_quantity', 'is_available')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_featured', 'is_active', 'display_order', 'product_count_display')
    list_editable = ('is_featured', 'is_active', 'display_order')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def product_count_display(self, obj):
        return obj.products.count()
    product_count_display.short_description = "Products"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'formatted_price', 'stock_status_badge', 'is_available', 'is_featured', 'is_bestseller', 'is_new')
    list_editable = ('is_available', 'is_featured', 'is_bestseller', 'is_new')
    list_filter = ('category', 'brand', 'is_available', 'is_featured', 'is_bestseller', 'is_new', 'is_on_sale')
    search_fields = ('name', 'sku', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "sku", "category", "brand", "short_description", "description")
        }),
        ("Pricing & Inventory", {
            "fields": (("price", "compare_at_price", "cost_price"), ("stock_quantity", "low_stock_threshold", "is_available"))
        }),
        ("Product Badges & Visibility", {
            "fields": (("is_featured", "is_bestseller", "is_new", "is_on_sale"),)
        }),
        ("Clinical / Detailed Specs", {
            "classes": ("collapse",),
            "fields": ("features", "specifications", "how_to_use", "size_guide", "weight", "dimensions")
        }),
        ("SEO Meta Info", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description")
        }),
        ("Audit Dates", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

    def formatted_price(self, obj):
        return f"KSh {obj.price:,.2f}"
    formatted_price.short_description = "Price"
    formatted_price.admin_order_field = "price"

    def stock_status_badge(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color: #ef4444; font-weight: bold;">Out of Stock (0)</span>')
        elif obj.stock_quantity <= obj.low_stock_threshold:
            return format_html('<span style="color: #f59e0b; font-weight: bold;">Low Stock ({})</span>', obj.stock_quantity)
        return format_html('<span style="color: #10b981;">In Stock ({})</span>', obj.stock_quantity)
    stock_status_badge.short_description = "Stock"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'display_order', 'created_at')
    list_filter = ('is_primary',)
    search_fields = ('product__name', 'alt_text')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price_adjustment', 'stock_quantity', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('product__name', 'name')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'rating', 'approved', 'verified_purchase', 'created_at')
    list_editable = ('approved',)
    list_filter = ('rating', 'approved', 'verified_purchase', 'created_at')
    search_fields = ('product__name', 'customer_name', 'customer_email', 'comment')
