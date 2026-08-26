from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, CustomerAddress
from apps.orders.forms import normalize_kenyan_phone

User = get_user_model()


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password (min. 8 characters)', 'required': True}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password', 'required': True}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 0719 160 398', 'required': True}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address', 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username / Handle', 'required': True}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        normalized = normalize_kenyan_phone(phone)
        if len(normalized) != 12:
            raise forms.ValidationError("Please enter a valid 10-digit Kenyan phone number (e.g. 0719160398).")
        return normalized

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data


class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username or Email', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password', 'required': True}))


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    email = forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'})

    class Meta:
        model = UserProfile
        fields = ['phone', 'county', 'town_city', 'address', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'County'}),
            'town_city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Town / City'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Estate / Street / House No.'}),
        }


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['title', 'recipient_name', 'phone', 'county', 'town_city', 'estate_address', 'is_default']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Home, Office, Clinic'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Recipient Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact Phone Number'}),
            'county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'County'}),
            'town_city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Town / City'}),
            'estate_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Detailed Address / House / Building'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
