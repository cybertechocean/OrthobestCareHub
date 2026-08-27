from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Service, BlogCategory, BlogPost, FAQ, LegalPage

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('title', 'icon_name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'read_time_minutes', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(LegalPage)
class LegalPageAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
