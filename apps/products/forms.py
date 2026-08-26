from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['customer_name', 'customer_email', 'rating', 'title', 'comment']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name', 'required': True}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your.email@example.com', 'required': True}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Summary of your experience'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Write your detailed review here...', 'required': True}),
        }
