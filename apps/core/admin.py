from django.contrib import admin
from .models import SiteSettings, HomeBanner, TrustBadge

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand & Contact Info", {
            "fields": ("site_name", "site_domain", "tagline", "phone_primary", "phone_secondary", "whatsapp_number", "contact_email", "physical_address", "business_hours")
        }),
        ("Announcement Bar", {
            "fields": ("announcement_bar_enabled", "announcement_bar_text", "announcement_bar_link")
        }),
        ("Homepage Hero Content", {
            "fields": ("hero_headline", "hero_subheadline", "hero_primary_cta_text", "hero_primary_cta_link", "hero_secondary_cta_text", "hero_secondary_cta_link", "hero_image")
        }),
        ("Branding Assets", {
            "fields": ("logo", "favicon")
        }),
        ("Compliance & Delivery", {
            "fields": ("medical_disclaimer", "currency_symbol", "currency_code", "free_delivery_threshold")
        }),
        ("Social Media", {
            "fields": ("facebook_url", "instagram_url", "tiktok_url", "twitter_url", "youtube_url")
        }),
        ("SEO & Tracking", {
            "fields": ("default_meta_title", "default_meta_description", "google_analytics_id", "meta_pixel_id")
        }),
    )

    def has_add_permission(self, request):
        # Only allow 1 instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'display_order', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'badge_text')


@admin.register(TrustBadge)
class TrustBadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'icon_svg', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
