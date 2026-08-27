from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import UserProfile, CustomerAddress

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ('user', 'phone', 'county', 'town_city', 'is_email_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'county', 'town_city')
    list_filter = ('is_email_verified', 'county')


@admin.register(CustomerAddress)
class CustomerAddressAdmin(ModelAdmin):
    list_display = ('title', 'user', 'recipient_name', 'phone', 'county', 'town_city', 'is_default')
    list_filter = ('is_default', 'county')
    search_fields = ('user__username', 'recipient_name', 'phone', 'estate_address')
