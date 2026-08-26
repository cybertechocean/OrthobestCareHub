from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View

from .models import Service, BlogPost, BlogCategory, FAQ, LegalPage
from apps.core.models import SiteSettings, TrustBadge


class AboutView(TemplateView):
    template_name = "content_hub/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trust_badges'] = TrustBadge.objects.filter(is_active=True)
        return context


class ServicesListView(ListView):
    model = Service
    template_name = "content_hub/services.html"
    context_object_name = "services"
    queryset = Service.objects.filter(is_active=True)


class BlogListView(ListView):
    model = BlogPost
    template_name = "content_hub/blog_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = BlogPost.objects.filter(status='published').select_related('category', 'author')
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "content_hub/blog_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(status='published').select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['related_posts'] = BlogPost.objects.filter(
            category=post.category, 
            status='published'
        ).exclude(id=post.id)[:3]
        return context


class FAQListView(ListView):
    model = FAQ
    template_name = "content_hub/faq.html"
    context_object_name = "faqs"

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('category', 'display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group FAQs by Category
        categories = {}
        for faq in self.get_queryset():
            if faq.category not in categories:
                categories[faq.category] = []
            categories[faq.category].append(faq)
        context['grouped_faqs'] = categories
        return context


class LegalPageView(View):
    def get(self, request, slug):
        page, created = LegalPage.objects.get_or_create(
            slug=slug,
            defaults={
                'title': slug.replace('-', ' ').title(),
                'content': f"Detailed policy guidelines for {slug.replace('-', ' ').title()} will be published here. Please contact our administrative support at info@orthobestcarehub.co.ke for inquiries."
            }
        )
        return render(request, "content_hub/legal_page.html", {'page': page})
