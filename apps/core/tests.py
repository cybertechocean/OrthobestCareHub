from django.test import TestCase
from django.urls import reverse
from apps.core.models import SiteSettings

class CoreAndMiddlewareTest(TestCase):
    def setUp(self):
        self.settings = SiteSettings.get_settings()

    def test_homepage_view(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Orthobest")

    def test_robots_txt(self):
        response = self.client.get(reverse('core:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disallow: /admin/")
        self.assertContains(response, "Sitemap:")

    def test_sitemap_xml(self):
        response = self.client.get(reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_legacy_path_redirect(self):
        response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/about/')

        response = self.client.get('/product-category/mobility-aids/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/shop/category/mobility-aids/')


class HeroCarouselTests(TestCase):
    def setUp(self):
        from apps.core.models import HeroSlide, HeroSlideBenefit, HeroCarouselSettings
        
        self.slide1 = HeroSlide.objects.create(
            title="Main Hero Slide",
            badge_icon="✦",
            badge_text="KENYA'S #1 ORTHOPEDIC STORE",
            heading="SUPPORT YOUR MOVEMENT.\nLIVE WITH CONFIDENCE.",
            description="Explore Kenya's highest quality braces.",
            primary_button_text="Shop Products →",
            primary_button_url="/shop/",
            secondary_button_text="Talk to a Specialist",
            secondary_button_url="/contact/",
            order=1,
            is_active=True
        )
        self.benefit1 = HeroSlideBenefit.objects.create(
            hero_slide=self.slide1,
            icon="✓",
            text="Medical Graded",
            order=1,
            is_active=True
        )
        self.benefit2 = HeroSlideBenefit.objects.create(
            hero_slide=self.slide1,
            icon="✓",
            text="M-Pesa Friendly",
            order=2,
            is_active=True
        )

        self.slide2 = HeroSlide.objects.create(
            title="Wheelchair Promotion",
            badge_icon="♿",
            badge_text="WHEELCHAIR SPECIALS",
            heading="PREMIUM MOBILITY GEAR",
            description="Lightweight and electric options.",
            order=2,
            is_active=True
        )

        self.inactive_slide = HeroSlide.objects.create(
            title="Inactive Promo",
            heading="EXPIRED PROMO",
            order=3,
            is_active=False
        )

        self.settings = HeroCarouselSettings.get_settings()
        self.settings.autoplay = True
        self.settings.autoplay_speed = 5000
        self.settings.save()

    def test_hero_models(self):
        self.assertEqual(str(self.slide1), "Main Hero Slide")
        self.assertTrue(self.slide1.has_primary_cta)
        self.assertTrue(self.slide1.has_secondary_cta)
        self.assertEqual(str(self.benefit1), "✓ Medical Graded")
        self.assertEqual(self.slide1.benefits.count(), 2)

    def test_homepage_renders_active_slides_only(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SUPPORT YOUR MOVEMENT.")
        self.assertContains(response, "PREMIUM MOBILITY GEAR")
        self.assertNotContains(response, "EXPIRED PROMO")
        self.assertContains(response, "Medical Graded")
        self.assertContains(response, "M-Pesa Friendly")
        self.assertContains(response, "heroCarousel")
        self.assertContains(response, "hero-nav-btn")
        self.assertContains(response, "hero-dot")

    def test_hero_empty_fallback(self):
        from apps.core.models import HeroSlide
        HeroSlide.objects.all().delete()
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hero-carousel-section")

