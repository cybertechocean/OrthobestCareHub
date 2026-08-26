import math
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    icon_name = models.CharField(max_length=80, blank=True, default="activity", help_text="Lucide/Feather icon name e.g. activity, shield, heart, wheelchair, bone")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} | Orthobest Care Hub Kenya"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        return self.products.filter(is_available=True).count()


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, help_text="Stock Keeping Unit e.g. OBC-KB-001")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    
    short_description = models.CharField(max_length=400, help_text="Concise summary displayed on product cards and header")
    description = models.TextField(help_text="Full detailed product overview")
    features = models.TextField(blank=True, help_text="Bullet points or key features list")
    specifications = models.TextField(blank=True, help_text="Technical specifications (material, size, dimensions, weight)")
    how_to_use = models.TextField(blank=True, help_text="Usage & maintenance instructions")
    size_guide = models.TextField(blank=True, help_text="Sizing measurement guide if applicable")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], help_text="Selling price in KSh")
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)], help_text="Original strike-through price if discounted")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)], help_text="Internal cost price for margin calculation")
    
    stock_quantity = models.PositiveIntegerField(default=10)
    low_stock_threshold = models.PositiveIntegerField(default=3)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Weight in Kilograms (kg)")
    dimensions = models.CharField(max_length=100, blank=True, help_text="Dimensions e.g. 50 x 30 x 20 cm")
    
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['price']),
            models.Index(fields=['is_featured', 'is_bestseller', 'is_new']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if self.compare_at_price and self.compare_at_price > self.price:
            self.is_on_sale = True
        else:
            self.is_on_sale = False
        if not self.meta_title:
            self.meta_title = f"{self.name} | Buy Online in Kenya | Orthobest Care Hub"
        if not self.meta_description:
            self.meta_description = self.short_description[:160] if self.short_description else self.name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    @property
    def in_stock(self):
        return self.is_available and self.stock_quantity > 0

    @property
    def is_low_stock(self):
        return self.in_stock and self.stock_quantity <= self.low_stock_threshold

    @property
    def discount_percentage(self):
        if self.compare_at_price and self.compare_at_price > self.price:
            diff = self.compare_at_price - self.price
            return int(round((diff / self.compare_at_price) * 100))
        return 0

    @property
    def average_rating(self):
        approved_reviews = self.reviews.filter(approved=True)
        if approved_reviews.exists():
            avg = approved_reviews.aggregate(models.Avg('rating'))['rating__avg']
            return round(avg, 1) if avg else 5.0
        return 5.0

    @property
    def review_count(self):
        return self.reviews.filter(approved=True).count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-is_primary', 'id']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = f"{self.product.name} - Orthobest Care Hub Kenya"
        if self.is_primary:
            # Ensure no other image is primary for this product
            ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=150, help_text="e.g. Size: Large, Side: Left, Color: Black")
    sku_modifier = models.CharField(max_length=50, blank=True, help_text="e.g. -L or -R")
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional price or discount for this variant (+/- KSh)")
    stock_quantity = models.PositiveIntegerField(default=5)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def effective_price(self):
        return self.product.price + self.price_adjustment


class ProductReview(models.Model):
    RATING_CHOICES = (
        (5, '★★★★★ (5/5) Excellent'),
        (4, '★★★★☆ (4/5) Very Good'),
        (3, '★★★☆☆ (3/5) Average'),
        (2, '★★☆☆☆ (2/5) Poor'),
        (1, '★☆☆☆☆ (1/5) Terrible'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    verified_purchase = models.BooleanField(default=False)
    approved = models.BooleanField(default=True, help_text="Approve this review for public display")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"{self.rating}★ by {self.customer_name} on {self.product.name}"
