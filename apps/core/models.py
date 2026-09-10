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
    facebook_url = models.URLField(blank=True, default="https://facebook.com/Orthobestcarehab")
    instagram_url = models.URLField(blank=True, default="https://instagram.com/Orthobestcarehab")
    tiktok_url = models.URLField(blank=True, default="https://tiktok.com/@Orthobestcarehab")
    twitter_url = models.URLField(blank=True, default="https://x.com/Orthobestcarehab")
    youtube_url = models.URLField(blank=True, default="https://youtube.com/@Orthobestcarehab")
    
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


class HeroSlide(models.Model):
    title = models.CharField(
        max_length=200, 
        help_text="Internal slide name for Django Admin management (e.g. Homepage Hero - Orthopedic Store)"
    )
    badge_text = models.CharField(
        max_length=120, 
        default="KENYA'S #1 ORTHOPEDIC & REHAB STORE",
        help_text="Eyebrow / pill badge text displayed above the headline"
    )
    badge_icon = models.CharField(
        max_length=50, 
        default="✦", 
        blank=True,
        help_text="Icon or symbol prefix for the badge (e.g. ✦, ✨, 🩺)"
    )
    heading = models.TextField(
        default="SUPPORT YOUR MOVEMENT.\nLIVE WITH CONFIDENCE.",
        help_text="Main large hero heading. Line breaks entered here will be preserved on the frontend."
    )
    description = models.TextField(
        default="Explore Kenya's highest quality orthopedic braces, rehabilitation equipment, manual & electric wheelchairs, and clinical homecare essentials.",
        help_text="Supporting paragraph / marketing message"
    )
    primary_button_text = models.CharField(
        max_length=100, 
        default="Shop Products →", 
        blank=True,
        help_text="Text for primary button (leave blank to hide)"
    )
    primary_button_url = models.CharField(
        max_length=255, 
        default="/shop/", 
        blank=True,
        help_text="Internal or external URL for primary button"
    )
    secondary_button_text = models.CharField(
        max_length=100, 
        default="Talk to a Specialist", 
        blank=True,
        help_text="Text for secondary button (leave blank to hide)"
    )
    secondary_button_url = models.CharField(
        max_length=255, 
        default="/contact/", 
        blank=True,
        help_text="Internal or external URL for secondary button"
    )
    image = models.ImageField(
        upload_to="hero_slides/", 
        blank=True, 
        null=True,
        help_text="Featured visual image for the right side of the hero"
    )
    image_alt_text = models.CharField(
        max_length=255, 
        blank=True, 
        default="Orthobest Care Hub Orthopedic & Rehabilitation Products Nairobi Kenya",
        help_text="Accessible description for screen readers and SEO"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Display order in the carousel (ascending order: 0, 1, 2...)"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Check to display this slide on the live website"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return self.title or self.heading[:50]

    @property
    def has_primary_cta(self):
        return bool(self.primary_button_text and self.primary_button_url)

    @property
    def has_secondary_cta(self):
        return bool(self.secondary_button_text and self.secondary_button_url)


class HeroSlideBenefit(models.Model):
    hero_slide = models.ForeignKey(
        HeroSlide, 
        related_name='benefits', 
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=150, 
        help_text="Trust/benefit message (e.g. Medical Graded, M-Pesa Friendly, Doorstep Delivery)"
    )
    icon = models.CharField(
        max_length=50, 
        default="✓", 
        blank=True,
        help_text="Symbol or checkmark prefix"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Hero Slide Benefit"
        verbose_name_plural = "Hero Slide Benefits"

    def __str__(self):
        return f"{self.icon} {self.text}".strip()


class HeroCarouselSettings(models.Model):
    autoplay = models.BooleanField(
        default=True, 
        help_text="Enable automatic slide transitions"
    )
    autoplay_speed = models.PositiveIntegerField(
        default=5500, 
        help_text="Time in milliseconds between slide transitions (e.g. 5000 = 5 seconds)"
    )
    show_arrows = models.BooleanField(
        default=True, 
        help_text="Show navigation arrow controls when multiple slides exist"
    )
    show_indicators = models.BooleanField(
        default=True, 
        help_text="Show slide dot indicators at the bottom"
    )
    pause_on_hover = models.BooleanField(
        default=True, 
        help_text="Pause autoplay when hovering with mouse or touching on mobile"
    )
    transition_speed = models.PositiveIntegerField(
        default=600, 
        help_text="Slide animation duration in milliseconds (e.g. 600)"
    )
    loop_slides = models.BooleanField(
        default=True, 
        help_text="Loop back to the first slide after the last slide"
    )

    class Meta:
        verbose_name = "Hero Carousel Settings"
        verbose_name_plural = "Hero Carousel Settings"

    def __str__(self):
        return "Hero Carousel Configuration"

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(id=1)
        return settings

