from django.urls import path
from .views import HomeView, robots_txt_view

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
]
