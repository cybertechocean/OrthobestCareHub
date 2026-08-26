import os
from django.http import HttpResponsePermanentRedirect

class LegacyDomainRedirectMiddleware:
    """
    Handles 301 Permanent Redirects for:
    1. Requests arriving on the old domain (orthobestcarerehab.co.ke) to the new domain (orthobestcarehub.co.ke).
    2. Legacy URL mapping paths (e.g. /product-category/..., /about-us/, /contact-us/).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.old_domain = os.environ.get("OLD_DOMAIN", "orthobestcarerehab.co.ke").lower()
        self.new_domain = os.environ.get("SITE_DOMAIN", "orthobestcarehub.co.ke").lower()
        
        # Legacy path mappings
        self.path_map = {
            '/about-us/': '/about/',
            '/about-us': '/about/',
            '/contact-us/': '/contact/',
            '/contact-us': '/contact/',
            '/product-category/mobility-aids/': '/shop/category/mobility-aids/',
            '/product-category/orthopedic-supports/': '/shop/category/orthopedic-supports/',
            '/product-category/rehabilitation/': '/shop/category/rehabilitation-equipment/',
            '/product-category/hospital-furniture/': '/shop/category/medical-furniture/',
            '/product-category/home-care/': '/shop/category/home-care/',
        }

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        path = request.path

        # 1. Check path redirect map
        if path in self.path_map:
            new_path = self.path_map[path]
            return HttpResponsePermanentRedirect(new_path)
            
        # 2. Redirect /product-category/<slug>/ to /shop/category/<slug>/
        if path.startswith('/product-category/'):
            parts = path.strip('/').split('/')
            if len(parts) >= 2:
                slug = parts[1]
                return HttpResponsePermanentRedirect(f"/shop/category/{slug}/")

        # 3. If request is directed to the old domain, redirect to new domain with same path & query
        if self.old_domain in host:
            scheme = 'https' if request.is_secure() else 'http'
            query = f"?{request.META['QUERY_STRING']}" if request.META.get('QUERY_STRING') else ''
            new_url = f"{scheme}://{self.new_domain}{path}{query}"
            return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)
