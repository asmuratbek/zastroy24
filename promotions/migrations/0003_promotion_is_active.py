# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-24 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0002_auto_20171224_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439?'),
        ),
    ]