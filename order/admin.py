# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderRow


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['order_items', 'created_at', 'total_weight', 'name', 'email', 'phone', 'address', 'get_product_list', 'excel_file']

    list_display = ['created_at', 'name', 'email', 'phone', '__unicode__', 'address', 'excel_file']

    fieldsets = (
        (None, {
            'fields': (
                'is_ordered',
                'created_at',
                'name',
                'email',
                'phone',
                'address',
                'get_product_list',
                'total_weight',
                'excel_file',
            )
        }),
    )

    def get_product_list(self, obj):
        result = """
        <table>
        <thead>
        <tr>
            <th>Артикул</th>
            <th>Товар</th>
            <th></th>
            <th>Категория</th>
            <th>Количество</th>
            <th>Цена</th>
            <th>Стоимость</th>
        </tr>
        </thead>
        <tbody>
        """
        for item in obj.order_items.all():
            link = reverse('products:product_single', kwargs={'product_slug': item.product.slug})            
            result += """
            <tr>
                <td>%s</td>
                <td><a href="%s" target="_blank">%s</a><td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            """ % (item.product.article, link, item.product.title, item.product.category, item.count, item.product.get_price(), item.count*item.product.get_price())

        result += """
        </tbody>
        </table>
        """

        return mark_safe(result)

    get_product_list.short_description = 'Товары'

    def has_add_permission(self, request):
        return False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRow)