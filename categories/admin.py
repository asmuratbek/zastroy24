# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Brand, SubCategory


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent_category', 'is_active']
    search_fields = ['title', 'slug']
    list_filter = ['parent_category']

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
