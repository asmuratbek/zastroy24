# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import *


# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 12

class ProductPropertyAdmin(admin.TabularInline):
    model = ProductProperty
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'id']
    list_display = 'id title consumption price is_active category brand'.split()
    list_filter = ['created_at']
    list_editable = ['title', 'price', 'consumption']
    prepopulated_fields = {'slug': ('title',)}

    readonly_fields = ('is_stock',)

    inlines = (ProductImageAdmin, ProductPropertyAdmin)

class PriceListAdmin(admin.ModelAdmin):
    list_display = ['id', 'price_list']

admin.site.register(Product, ProductAdmin)
admin.site.register(AllProductProperties)
admin.site.register(PriceList, PriceListAdmin)
