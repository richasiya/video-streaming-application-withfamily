from django.contrib import admin
from .models import Category, Content


from .models import SiteConfig


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
	list_display = ('title', 'content_type', 'access_level', 'category', 'created_at')
	list_filter = ('content_type', 'access_level', 'category')
	search_fields = ('title', 'description')


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo')
