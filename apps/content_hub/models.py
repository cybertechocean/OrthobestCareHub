from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_summary = models.CharField(max_length=350)
    description = models.TextField(help_text="Full service overview and what clients can expect")
    icon_name = models.CharField(max_length=80, default="heart-pulse", help_text="e.g. heart-pulse, activity, shield, user-check")
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    excerpt = models.TextField(max_length=500, help_text="Brief summary shown on cards")
    content = models.TextField(help_text="Full article body (HTML or Markdown supported)")
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    read_time_minutes = models.PositiveIntegerField(default=4)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Article"
        verbose_name_plural = "Blog Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = f"{self.title} | Orthobest Care Hub Blog"
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('content_hub:blog_detail', kwargs={'slug': self.slug})


class FAQ(models.Model):
    CATEGORY_CHOICES = (
        ('General', 'General Questions'),
        ('Orders & Delivery', 'Orders & Kenya Delivery'),
        ('Products & Sizing', 'Products, Sizing & Advice'),
        ('Payments & M-Pesa', 'Payments & Safaricom M-Pesa'),
    )

    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'display_order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class LegalPage(models.Model):
    SLUG_CHOICES = (
        ('privacy-policy', 'Privacy Policy'),
        ('terms-conditions', 'Terms & Conditions'),
        ('shipping-policy', 'Shipping & Delivery Policy'),
        ('returns-refund-policy', 'Returns & Refund Policy'),
        ('cookie-policy', 'Cookie Policy'),
    )

    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=100, choices=SLUG_CHOICES, unique=True)
    content = models.TextField(help_text="Detailed legal terms and policy body")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Legal & Store Policy"
        verbose_name_plural = "Legal & Store Policies"

    def __str__(self):
        return self.title
