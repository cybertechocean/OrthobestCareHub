from django.urls import path
from .views import (
    AboutView, ServicesListView, BlogListView, BlogDetailView,
    FAQListView, LegalPageView
)

app_name = 'content_hub'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesListView.as_view(), name='services'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('faq/', FAQListView.as_view(), name='faq'),
    path('privacy-policy/', LegalPageView.as_view(), {'slug': 'privacy-policy'}, name='privacy_policy'),
    path('terms/', LegalPageView.as_view(), {'slug': 'terms-conditions'}, name='terms'),
    path('shipping-policy/', LegalPageView.as_view(), {'slug': 'shipping-policy'}, name='shipping_policy'),
    path('returns-policy/', LegalPageView.as_view(), {'slug': 'returns-refund-policy'}, name='returns_policy'),
    path('cookie-policy/', LegalPageView.as_view(), {'slug': 'cookie-policy'}, name='cookie_policy'),
]
