# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from io import BytesIO

from product.utils import rename_file, add_watermark, get_wt_image_url


# Create your models here.


class Post(models.Model):
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'

    is_active = models.BooleanField(default=True, verbose_name='Активная новость?')

    title = models.CharField(max_length=255, verbose_name='Наименование новости', help_text='Он же и meta_title')
    slug = models.CharField(max_length=255, verbose_name='slug', help_text='Нужен для URL')

    preview = models.ImageField(upload_to='news/', verbose_name='Предосмотр новости', null=True, blank=True)
    short_description = models.TextField(verbose_name='Краткое описание', null=True, max_length=160)
    content = RichTextUploadingField(verbose_name='Тело новости')

    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __unicode__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.preview:
            new_img_obj = Image.open(self.preview)
            t_title = self.title + '.png'
            new_img_bytes = BytesIO()
            new_img_obj.save(new_img_bytes, format='PNG')

            self.preview.delete(save=False)
            self.preview.save(
                t_title,
                content=ContentFile(new_img_bytes.getvalue()),
                save=False
            )
        super(Post, self).save(*args, **kwargs)
        if self.preview:
            try:
                add_watermark(self.preview.path, 'MYBRANDS.KG')
            except:
                pass