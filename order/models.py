# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.urls import reverse


class Order(models.Model):
    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


    order_items = models.ManyToManyField('OrderRow', verbose_name='Элементы заказа', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_weight = models.CharField(max_length=255, verbose_name='Общий вес', null=True)
    is_ordered = models.BooleanField(verbose_name='Заказ отправлен?', default=False)

    name = models.CharField(verbose_name='Имя заказчика', null=True, blank=True, max_length=255)
    email = models.CharField(max_length=255, verbose_name='E-Mail', null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(max_length=1000, verbose_name='Адрес оставки', null=True)
    comment = models.TextField(max_length=1000, verbose_name='Комментарий', null=True, blank=True)

    excel_file = models.FileField(upload_to='order/', verbose_name='Excel файл', null=True, blank=True)

    def get_order_full_price(self):
        price = 0
        for item in self.order_items.all():
            price = price + item.get_price()
        return price

    def __unicode__(self):
        return str(len(self.order_items.all())) + ' вида товаров на ' + str(self.get_order_full_price()) + ' руб.'


class OrderRow(models.Model):
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    product = models.ForeignKey('product.Product', verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Количество')

    def __unicode__(self):
        return self.product.title + ' | ' + str(self.count) + ' | ' + str(self.product.price * self.count)

    def get_price(self):
        return self.product.price * self.count
