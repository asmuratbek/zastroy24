# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-24 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_productproperty_value_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productproperty',
            name='value_type',
            field=models.CharField(blank=True, help_text='\u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u043a\u0433', max_length=255, null=True, verbose_name='\u0415\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f'),
        ),
    ]