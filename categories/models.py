# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext_lazy as _

from product.utils import rename_file
from django.db import models


# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    CHOICES = (
        ('dry_mixture', _('Сухая смесь')),
        ('ceiling', _('Потолок'))
    )

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.CharField(max_length=255, verbose_name='slug',
                            help_text='Нужен для URL')
    description = models.TextField(verbose_name='Описание категории', null=True, blank=True,
                                   help_text='Нужен для SEO')
    thumbnail = models.ImageField(upload_to='categories/', verbose_name='Иконка', null=True, blank=True)
    seo_thumbnail = models.ImageField(upload_to='categories/seo/', verbose_name='Картинка(Для SEO)', null=True,
                                      blank=True)

    is_active = models.BooleanField(default=True, verbose_name='Активный?')
    parent_category = models.ForeignKey('Category', verbose_name='Родительская категория', null=True, blank=True)
    calculation_category = models.CharField(max_length=255, choices=CHOICES, verbose_name='Категория для калькулятора', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.thumbnail:
            rename_file(self.thumbnail, '%s_thumbnail_%s.png' % (self.slug, str(datetime.datetime.now())))
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = 'Подкатегории'
        verbose_name = 'подкатегорию'

    title = models.CharField(max_length=255, verbose_name='Название')

    def __unicode__(self):
        return self.title


class Brand(models.Model):
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.CharField(max_length=255, verbose_name='slug',
                            help_text='Нужен для URL')

    description = models.TextField(verbose_name='Описание бренда',
                                   help_text='Нужен для SEO', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='brands/', verbose_name='Картинка', null=True, blank=True)
    is_show = models.BooleanField(default=True, verbose_name='Показывать на главной странице?')
    is_active = models.BooleanField(default=True, verbose_name='Активный?')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.thumbnail:
            rename_file(self.thumbnail, '%s_thumbnail_%s.png' % (self.slug, str(datetime.datetime.now())))
        super(Brand, self).save(*args, **kwargs)
