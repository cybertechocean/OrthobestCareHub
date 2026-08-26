from django.urls import path
from .views import ContactView, NewsletterSubscribeAjaxView

app_name = 'leads'

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('api/newsletter/subscribe/', NewsletterSubscribeAjaxView.as_view(), name='newsletter_subscribe'),
]
