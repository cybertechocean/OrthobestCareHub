from django import forms
from .models import ContactMessage, NewsletterSubscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 0719 160 398'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'How can we help you?', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Tell us more about the product or guidance you need...', 'required': True}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'newsletter-input', 'placeholder': 'Enter your email address', 'required': True}),
        }
