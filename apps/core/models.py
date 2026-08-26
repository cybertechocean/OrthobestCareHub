from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="Orthobest Care Hub")
    site_domain = models.CharField(max_length=200, default="orthobestcarehub.co.ke")
    tagline = models.CharField(max_length=300, default="Kenya's Premier Destination for Orthopedic, Rehabilitation & Mobility Solutions")
    
    # Contact Details
    phone_primary = models.CharField(max_length=50, default="+254 719 160 398")
    phone_secondary = models.CharField(max_length=50, default="+254 727 480 198", blank=True)
    whatsapp_number = models.CharField(max_length=50, default="254798246811", help_text="Number in international format without + or spaces (e.g. 254798246811)")
    contact_email = models.EmailField(default="info@orthobestcarehub.co.ke")
    physical_address = models.TextField(default="Mfangano Street, Travis Building, 3rd Floor, Room C37, Wing C (near Quickmart), Nairobi CBD, Kenya")
    business_hours = models.CharField(max_length=255, default="Mon - Fri: 9:00 AM - 5:00 PM | Sat: 9:00 AM - 3:00 PM | Sun: Closed")
    
    # Announcement Bar
    announcement_bar_enabled = models.BooleanField(default=True)
    announcement_bar_text = models.CharField(max_length=300, default="🚚 Fast, Reliable Delivery Across Kenya | Free Consultations on Product Selection!")
    announcement_bar_link = models.CharField(max_length=300, blank=True, default="/shop/")
    
    # Currency
    currency_symbol = models.CharField(max_length=10, default="KSh")
    currency_code = models.CharField(max_length=10, default="KES")
    
    # Hero Section Content
    hero_headline = models.CharField(max_length=255, default="SUPPORT YOUR MOVEMENT. LIVE WITH CONFIDENCE.")
    hero_subheadline = models.TextField(default="Premium orthopedic supports, rehabilitation devices, wheelchairs, and healthcare equipment curated to restore comfort, strength, and independence.")
    hero_primary_cta_text = models.CharField(max_length=100, default="Shop Products")
    hero_primary_cta_link = models.CharField(max_length=200, default="/shop/")
    hero_secondary_cta_text = models.CharField(max_length=100, default="Talk to a Specialist")
    hero_secondary_cta_link = models.CharField(max_length=200, default="/contact/")
    
    # Media Assets
    logo = models.ImageField(upload_to="site/logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/favicon/", blank=True, null=True)
    hero_image = models.ImageField(upload_to="site/hero/", blank=True, null=True)
    
    # Trust & Compliance
    medical_disclaimer = models.TextField(
        default="Product information is provided for general informational purposes and does not replace professional medical diagnosis or advice. Always consult a licensed healthcare practitioner or physiotherapist when selecting specialized rehabilitation gear."
    )
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00, help_text="Order amount above which standard delivery is free (if applicable)")
    
    # Social Links
    facebook_url = models.URLField(blank=True, default="https://facebook.com")
    instagram_url = models.URLField(blank=True, default="https://instagram.com")
    tiktok_url = models.URLField(blank=True, default="https://tiktok.com")
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Analytics / SEO
    default_meta_title = models.CharField(max_length=255, default="Orthobest Care Hub | Kenya's Trusted Orthopedic & Rehabilitation Store")
    default_meta_description = models.TextField(default="Buy premium wheelchairs, knee braces, cervical collars, walking aids, physiotherapy tools, and hospital beds in Nairobi, Kenya. Fast countrywide delivery.")
    google_analytics_id = models.CharField(max_length=50, blank=True)
    meta_pixel_id = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class HomeBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    badge_text = models.CharField(max_length=100, blank=True, default="Featured Promotion")
    button_text = models.CharField(max_length=100, default="Shop Now")
    button_link = models.CharField(max_length=255, default="/shop/")
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    bg_gradient = models.CharField(max_length=100, default="linear-gradient(135deg, #0d9488 0%, #065f46 100%)")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Home Banner"
        verbose_name_plural = "Home Banners"

    def __str__(self):
        return self.title


class TrustBadge(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255)
    icon_svg = models.CharField(max_length=100, default="shield-check", help_text="Icon identifier (e.g. shield-check, truck, headset, badge-check)")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Trust Badge"
        verbose_name_plural = "Trust Badges"

    def __str__(self):
        return self.title
