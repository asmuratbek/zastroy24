# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.


class Promotion(models.Model):
    class Meta:
        verbose_name = 'акцию'
        verbose_name_plural = 'Акции'

    is_active = models.BooleanField(default=True, verbose_name='Активный?')
    product = models.ForeignKey('product.Product', verbose_name='Товар на который действует акция')
    title = models.CharField(max_length=255, verbose_name='Название акции')
    slug = models.CharField(max_length=255, verbose_name='slug', null=True)
    description = RichTextUploadingField(verbose_name='Описание акции')
    expires_date = models.DateField(null=True, blank=True, verbose_name='Число до которого будет действовать акция')

    def __unicode__(self):
        return self.title
