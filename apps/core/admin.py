from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    SiteSettings, HomeBanner, TrustBadge,
    HeroSlide, HeroSlideBenefit, HeroCarouselSettings
)


class HeroSlideBenefitInline(TabularInline):
    model = HeroSlideBenefit
    extra = 3
    fields = ('icon', 'text', 'order', 'is_active')


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = (
        'image_thumbnail', 'title', 'badge_preview',
        'heading_preview', 'order', 'is_active', 'benefits_count', 'updated_at'
    )
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'heading', 'description', 'badge_text')
    inlines = [HeroSlideBenefitInline]
    readonly_fields = ('image_preview', 'created_at', 'updated_at')

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                ("order", "is_active")
            )
        }),
        ("Hero Eyebrow / Badge", {
            "fields": (
                ("badge_icon", "badge_text"),
            )
        }),
        ("Headline & Marketing Message", {
            "fields": (
                "heading",
                "description",
            )
        }),
        ("Call-to-Action Buttons", {
            "fields": (
                ("primary_button_text", "primary_button_url"),
                ("secondary_button_text", "secondary_button_url"),
            )
        }),
        ("Featured Visual & Accessibility", {
            "fields": (
                "image",
                "image_preview",
                "image_alt_text",
            )
        }),
        ("System Timestamps", {
            "fields": (
                ("created_at", "updated_at"),
            ),
            "classes": ("collapse",)
        }),
    )

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />',
                obj.image.url
            )
        return format_html(
            '<span style="display:inline-block; width:48px; height:48px; line-height:48px; text-align:center; background:#f1f5f9; color:#94a3b8; border-radius:8px; font-size:12px;">No Img</span>'
        )
    image_thumbnail.short_description = "Image"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin: 10px 0;"><img src="{}" style="max-height: 200px; max-width: 100%; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" /></div>',
                obj.image.url
            )
        return "No image uploaded yet."
    image_preview.short_description = "Current Image Preview"

    def badge_preview(self, obj):
        if obj.badge_text:
            return format_html(
                '<span style="background: rgba(251, 212, 32, 0.15); border: 1px solid #C99935; color: #B47A14; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}</span>',
                obj.badge_icon or "",
                obj.badge_text
            )
        return "-"
    badge_preview.short_description = "Badge"

    def heading_preview(self, obj):
        if obj.heading:
            text = obj.heading.replace("\n", " ")
            return text[:45] + ("..." if len(text) > 45 else "")
        return "-"
    heading_preview.short_description = "Heading"

    def benefits_count(self, obj):
        return obj.benefits.count()
    benefits_count.short_description = "Benefits"


@admin.register(HeroCarouselSettings)
class HeroCarouselSettingsAdmin(ModelAdmin):
    fieldsets = (
        ("Playback & Timing Controls", {
            "fields": (
                ("autoplay", "autoplay_speed"),
                ("transition_speed", "loop_slides"),
                "pause_on_hover",
            )
        }),
        ("Navigation Controls", {
            "fields": (
                ("show_arrows", "show_indicators"),
            )
        }),
    )

    def has_add_permission(self, request):
        return not HeroCarouselSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
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
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeBanner)
class HomeBannerAdmin(ModelAdmin):
    list_display = ('title', 'badge_text', 'display_order', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'badge_text')


@admin.register(TrustBadge)
class TrustBadgeAdmin(ModelAdmin):
    list_display = ('title', 'subtitle', 'icon_svg', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
