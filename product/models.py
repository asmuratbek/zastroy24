# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import os

from django.contrib.postgres.fields import JSONField
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from MyBrands import settings
from .utils import add_watermark, rename_file, get_wt_image_url
from django.core.validators import MinValueValidator


# Create your models here.

class PriceList(models.Model):
    class Meta:
        verbose_name = 'прайс лист'
        verbose_name_plural = 'Прайс листы'

    price_list = models.FileField(upload_to='price_list/', verbose_name='Файл')

class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    article = models.CharField(max_length=255, verbose_name='Артикул', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.CharField(max_length=255, verbose_name='Slug', help_text='Нужен для URL')
    # description = models.TextField(max_length=10000, verbose_name='Описание', null=True, blank=True)
    description = RichTextUploadingField(verbose_name='Описание', null=True, blank=True)
    documentation = RichTextUploadingField(verbose_name='Документация', null=True, blank=True)
    weight = models.FloatField(default=0.0, verbose_name='Вес (кг)')
    consumption = models.FloatField(default=0.0, verbose_name='Расход в килограммах на метр куб')
    price = models.FloatField(verbose_name='Цена')
    main_image = models.ImageField(upload_to='products/', verbose_name='Главная картинка', null=True)
    discount = models.IntegerField(verbose_name='Скидка на товар', null=True, blank=True, default=0,
                                   help_text='''
                                   Если на товар появилась скидка, то впишите его сюда.<br>
                                   После того как вы впишите скидку цена везде станет с учётом скидки,<br>
                                   Поэтому менять поле "Цена" не нужно, если это не требуется
                                   ''')

    is_active = models.BooleanField(default=True, verbose_name='Активный?',
                                    help_text='''
                                    На сайте отображаются только те товары, которые помечены "Активным"!<br>
                                    Поэтому вместо того, чтобы удалить товар из базы просто уберите галочку "Активный"<br>
                                    После этого товар перестанет быть виден на сайте
                                    ''')
    is_available = models.BooleanField(default=True, verbose_name='Есть в наличии?')
    is_stock = models.BooleanField(default=False, verbose_name='Действует акция?')
    category = models.ForeignKey('categories.Category', verbose_name='Категория', null=True)
    brand = models.ForeignKey('categories.Brand', verbose_name='Бренд', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __unicode__(self):
        return self.title + ', ' + str(self.price) + ' руб.'

    def get_my_images(self):
        return [x for x in ProductImage.objects.filter(product=self).all()]

    def get_my_first_image(self):
        return ProductImage.objects.filter(product=self).first()

    def get_price(self):
        if self.discount > 0:
            return self.price - ((self.price * self.discount) / 100)
        return self.price

    def save(self, *args, **kwargs):
        self.is_stock = self.discount > 0
        super(Product, self).save(*args, **kwargs)


class Calculation(models.Model):
    category = models.ForeignKey('categories.Category')
    product = models.ForeignKey(Product)
    area = models.FloatField(default=0.0, )
    thickness = models.PositiveIntegerField()


class ProductImage(models.Model):
    class Meta:
        verbose_name_plural = 'Картинки для товаров'
        verbose_name = 'Картинка для товаров'

    product = models.ForeignKey('Product', verbose_name='Продукт', related_name='product_image', null=True, blank=True)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')

    def save(self, *args, **kwargs):
        rename_file(self.image, 'uploaded_at_' + str(datetime.datetime.now()) + '.png')
        super(ProductImage, self).save(*args, **kwargs)
        if self.image:
            try:
                add_watermark(self.image, settings.SITE_TITLE)
            except:
                pass

    def get_image_url(self):
        f, e = os.path.splitext(self.image.path)
        wt_image = '%s.wt%s' % (f, e)
        if os.path.isfile(wt_image):
            b, s = os.path.splitext(self.image.url)
            return '%s.wt%s' % (b, s)
        return self.image.url


class ProductSize(models.Model):
    class Meta(object):
        verbose_name_plural = 'Размеры'
        verbose_name = 'размер'
        ordering = ('sort_order',)

    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Передвинте мышкой')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    category = models.ForeignKey(
        'categories.Category',
        related_name='sizes',
        verbose_name='Категория',
        help_text='Категория, к которому пренадлежит этот размер'
    )
    sub_category = models.ForeignKey('categories.SubCategory', verbose_name='Подкатегория', null=True)

    def __unicode__(self):
        return self.title


class ProductColor(models.Model):
    class Meta:
        verbose_name_plural = 'Расцветка товара'
        verbose_name = 'цвет'

    color = models.CharField(max_length=255, verbose_name='Расцветка', blank=True, null=True)
    size = models.ManyToManyField('ProductSizeSettings', verbose_name='Размеры', blank=False)

    def display(self):
        if self.color:
            return '<span style="background: %s; padding: 10px; display: inline-block; vertical-align: middle;"></span> - [%s]' % (
                self.color, ','.join(x.size.title for x in self.size.all()))
        return 'Без цвета - [%s]' % ','.join(x.size.title for x in self.size.all())

    display.allow_tags = True

    def __unicode__(self):
        if self.color:
            return self.color + ' - ' + str(self.size.count()) + ' размеров'
        return 'Только одна расцветка - ' + str(self.size.count()) + ' размеров'


class ProductSizeSettings(models.Model):
    class Meta:
        verbose_name_plural = 'Склад'

    size = models.ForeignKey('ProductSize', verbose_name='Размер', null=True, blank=True)
    count = models.PositiveIntegerField(
        verbose_name='Количество на складе',
        help_text='''
            Внимание! Система может обновлять данные не корректно. 
            Просьба проверять инфорацию о наличии товара на складе <br>
            ''',
        validators=[MinValueValidator(0)]
    )

    def __unicode__(self):
        return '#' + str(self.id) + '|' + str(self.size) + '|' + str(self.count)


class ProductProperty(models.Model):
    class Meta:
        verbose_name_plural = 'Свойство товара'
        verbose_name = 'свойство'

    key = models.ForeignKey('AllProductProperties', verbose_name='Свойство', null=True)
    value = models.CharField(max_length=10000, verbose_name='Значение')
    value_type = models.CharField(max_length=255, verbose_name='Единица измерения', null=True, blank=True,
                                  help_text='Например, кг')
    prop_tip = models.TextField(max_length=10000, verbose_name='Подсказка для свойства!', null=True, blank=True)
    product = models.ForeignKey('Product', verbose_name='товар', null=True, related_name='property')

    def __unicode__(self):
        return self.key.title


class AllProductProperties(models.Model):
    class Meta:
        verbose_name_plural = 'Все свойства'
        verbose_name = 'свойство'

    title = models.CharField(max_length=255, verbose_name='Название')

    def __unicode__(self):
        return self.title
