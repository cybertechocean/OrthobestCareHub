"""
URL Configuration for Orthobest Care Hub.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from apps.core.sitemaps import (
    StaticViewSitemap, CategorySitemap,
    ProductSitemap, BlogPostSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'blog': BlogPostSitemap,
}

# Admin branding
admin.site.site_header = "Orthobest Care Hub Administration"
admin.site.site_title = "Orthobest Care Hub Portal"
admin.site.index_title = "Store & Catalog Operations Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Sitemaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Modular App URLs
    path('', include('apps.core.urls')),
    path('', include('apps.products.urls')),
    path('', include('apps.cart.urls')),
    path('', include('apps.orders.urls')),
    path('', include('apps.payments.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.content_hub.urls')),
    path('', include('apps.leads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
