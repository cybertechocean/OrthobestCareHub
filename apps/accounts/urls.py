from django.urls import path
from .views import (
    CustomerRegisterView, CustomerLoginView, CustomerLogoutView,
    AccountDashboardView, AccountOrdersView, AccountAddressesView, AccountProfileView
)

app_name = 'accounts'

urlpatterns = [
    path('account/register/', CustomerRegisterView.as_view(), name='register'),
    path('account/login/', CustomerLoginView.as_view(), name='login'),
    path('account/logout/', CustomerLogoutView.as_view(), name='logout'),
    path('account/', AccountDashboardView.as_view(), name='dashboard'),
    path('account/orders/', AccountOrdersView.as_view(), name='orders'),
    path('account/addresses/', AccountAddressesView.as_view(), name='addresses'),
    path('account/profile/', AccountProfileView.as_view(), name='profile'),
]
