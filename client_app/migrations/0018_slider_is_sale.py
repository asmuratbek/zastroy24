# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-25 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0017_auto_20171225_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='is_sale',
            field=models.BooleanField(default=False, verbose_name='\u0410\u043a\u0446\u0438\u044f?'),
        ),
    ]