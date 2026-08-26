from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from .forms import ContactForm, NewsletterForm
from .models import ContactMessage, NewsletterSubscriber


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "leads/contact.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received. Our clinical support team will contact you shortly.")
            return redirect('leads:contact')
        return render(request, "leads/contact.html", {'form': form})


class NewsletterSubscribeAjaxView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        if not email or '@' not in email:
            return JsonResponse({'success': False, 'message': 'Please provide a valid email address.'})

        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()

        return JsonResponse({
            'success': True,
            'message': 'Thank you for subscribing to Orthobest Care Hub wellness & product updates!'
        })
