from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.products.models import Product, Category
from apps.content_hub.models import BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'products:shop',
            'content_hub:about',
            'content_hub:services',
            'content_hub:blog_list',
            'content_hub:faq',
            'leads:contact',
            'content_hub:privacy_policy',
            'content_hub:terms',
            'content_hub:shipping_policy',
            'content_hub:returns_policy',
        ]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Product.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at
