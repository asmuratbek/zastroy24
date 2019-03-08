# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'is_read']

    readonly_fields = ['first_name', 'last_name', 'email', 'phone_number']

    def has_add_permission(self, request):
        return False


admin.site.register(Feedback, FeedbackAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']


class SliderAdmin(admin.ModelAdmin):
    list_display =  ['__unicode__', 'is_active']


class ReviewAdmin(admin.ModelAdmin):
    list_display = 'name email created_at is_active'.split()
    readonly_fields = 'name email message created_at'.split()


class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return True
        else:
            return False


admin.site.register(AdminEmails, EmailAdmin)
admin.site.register(About)
admin.site.register(Delivery)
admin.site.register(Slider, SliderAdmin)
admin.site.register(SeoText)
admin.site.register(Contact)
admin.site.register(OurTeam)
admin.site.register(AboutInNumbers)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Manufacturers, SiteSettingsAdmin)
admin.site.register(TermsOfSaleOfGoods, SiteSettingsAdmin)
admin.site.register(ReturnPolicy, SiteSettingsAdmin)
admin.site.register(RepairTips, SiteSettingsAdmin)

