from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=50, blank=True, help_text="Kenyan phone number")
    county = models.CharField(max_length=100, blank=True, default="Nairobi")
    town_city = models.CharField(max_length=100, blank=True, default="Nairobi")
    address = models.CharField(max_length=255, blank=True, help_text="Building, Road, Estate, House No.")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"


class CustomerAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_addresses")
    title = models.CharField(max_length=100, default="Home", help_text="e.g. Home, Office, Clinic")
    recipient_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    county = models.CharField(max_length=100, default="Nairobi")
    town_city = models.CharField(max_length=100, default="Nairobi")
    estate_address = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name = "Saved Address"
        verbose_name_plural = "Saved Addresses"

    def __str__(self):
        return f"{self.title}: {self.estate_address}, {self.town_city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            CustomerAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
