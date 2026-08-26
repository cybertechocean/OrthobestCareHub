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
