# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.


class PromotionAdmin(admin.ModelAdmin):
    list_display = 'title is_active'.split()
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Promotion, PromotionAdmin)
