# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'is_active', 'created_at']
    list_editable = ['title',]

    search_fields = ['title', 'id', 'content']

    list_filter = ['created_at', 'updated_at']

    ordering = ['title',]

    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Post, PostAdmin)
