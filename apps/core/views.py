from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import SiteSettings, HomeBanner, TrustBadge

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Import lazily to avoid circular dependencies
        from apps.products.models import Product, Category
        from apps.content_hub.models import BlogPost, Service

        context['banners'] = HomeBanner.objects.filter(is_active=True)
        context['trust_badges'] = TrustBadge.objects.filter(is_active=True)
        context['featured_categories'] = Category.objects.filter(is_featured=True, is_active=True)[:8]
        context['all_categories'] = Category.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(is_available=True, is_featured=True).select_related('category', 'brand').prefetch_related('images')[:8]
        context['bestseller_products'] = Product.objects.filter(is_available=True, is_bestseller=True).select_related('category', 'brand').prefetch_related('images')[:8]
        context['new_products'] = Product.objects.filter(is_available=True, is_new=True).select_related('category', 'brand').prefetch_related('images')[:8]
        context['recent_posts'] = BlogPost.objects.filter(status='published').select_related('category')[:3]
        context['services'] = Service.objects.filter(is_active=True)[:4]
        return context


def robots_txt_view(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /account/",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Disallow: /orders/",
        "Disallow: /payments/",
        "Disallow: /leads/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def custom_404_view(request, exception=None):
    return render(request, "core/404.html", status=404)


def custom_500_view(request):
    return render(request, "core/500.html", status=500)


def custom_403_view(request, exception=None):
    return render(request, "core/403.html", status=403)
