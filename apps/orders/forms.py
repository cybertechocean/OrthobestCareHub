import re
from django import forms
from .models import Order, DeliveryZone, Coupon


def normalize_kenyan_phone(phone_str):
    """Normalize phone string into Kenyan format (e.g. 254712345678 or 0712345678)"""
    digits = re.sub(r'\D', '', phone_str)
    if digits.startswith('0') and len(digits) == 10:
        return '254' + digits[1:]
    elif digits.startswith('254') and len(digits) == 12:
        return digits
    elif digits.startswith('7') and len(digits) == 9:
        return '254' + digits
    elif digits.startswith('1') and len(digits) == 9:
        return '254' + digits
    return digits


class CheckoutForm(forms.ModelForm):
    coupon_code = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input uppercase',
        'placeholder': 'Coupon code (e.g. WELCOME10)',
        'id': 'coupon_code_input'
    }))

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'county', 'town_city', 'estate_address', 'delivery_notes',
            'delivery_zone', 'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address (for order receipts)'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 0719 160 398 or 254719160398', 'required': True}),
            'county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'County e.g. Nairobi, Kiambu, Mombasa'}),
            'town_city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Town / City / Area'}),
            'estate_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Building, Road, House / Office Number', 'required': True}),
            'delivery_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Any specific landmark or directions for delivery rider'}),
            'delivery_zone': forms.Select(attrs={'class': 'form-select', 'required': True, 'id': 'delivery_zone_select'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-radio'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        normalized = normalize_kenyan_phone(phone)
        if len(normalized) != 12 or not normalized.startswith('254'):
            raise forms.ValidationError("Please enter a valid Kenyan phone number (e.g. 0719160398, 0110123456, or +254719160398).")
        return normalized


class OrderTrackForm(forms.Form):
    order_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-input uppercase',
        'placeholder': 'e.g. OBC-2026-1234',
        'required': True
    }))
    phone_or_email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Phone number or Email used during checkout',
        'required': True
    }))
