# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-22 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_category_parent_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='seo_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='categories/seo/', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430(\u0414\u043b\u044f SEO)'),
        ),
        migrations.AlterField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='\u0418\u043a\u043e\u043d\u043a\u0430'),
        ),
    ]
