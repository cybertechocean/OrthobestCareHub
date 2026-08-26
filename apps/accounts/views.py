from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import CustomerRegistrationForm, CustomerLoginForm, UserProfileForm, CustomerAddressForm
from .models import UserProfile, CustomerAddress
from apps.orders.models import Order

User = get_user_model()


class CustomerRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = CustomerRegistrationForm()
        return render(request, "accounts/register.html", {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # Update profile phone
            user.profile.phone = form.cleaned_data['phone']
            user.profile.save()

            login(request, user)
            messages.success(request, f"Welcome to Orthobest Care Hub, {user.first_name}!")
            return redirect('accounts:dashboard')

        return render(request, "accounts/register.html", {'form': form})


class CustomerLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = CustomerLoginForm()
        return render(request, "accounts/login.html", {'form': form, 'next': request.GET.get('next', '')})

    def post(self, request):
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.POST.get('next') or request.GET.get('next') or 'accounts:dashboard'
            return redirect(next_url)
        return render(request, "accounts/login.html", {'form': form})


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('core:home')

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('core:home')


class AccountDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
        addresses = CustomerAddress.objects.filter(user=request.user)[:3]
        return render(request, "accounts/dashboard.html", {
            'user': request.user,
            'recent_orders': orders,
            'addresses': addresses,
            'total_orders_count': Order.objects.filter(user=request.user).count()
        })


class AccountOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "accounts/orders.html", {'orders': orders})


class AccountAddressesView(LoginRequiredMixin, View):
    def get(self, request):
        addresses = CustomerAddress.objects.filter(user=request.user)
        form = CustomerAddressForm()
        return render(request, "accounts/addresses.html", {'addresses': addresses, 'form': form})

    def post(self, request):
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "New address saved successfully!")
            return redirect('accounts:addresses')
        addresses = CustomerAddress.objects.filter(user=request.user)
        return render(request, "accounts/addresses.html", {'addresses': addresses, 'form': form})


class AccountProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        form = UserProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': profile.phone,
            'county': profile.county,
            'town_city': profile.town_city,
            'address': profile.address,
        })
        return render(request, "accounts/profile.html", {'form': form})

    def post(self, request):
        profile = request.user.profile
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, "Your profile details have been updated.")
            return redirect('accounts:profile')
        return render(request, "accounts/profile.html", {'form': form})
