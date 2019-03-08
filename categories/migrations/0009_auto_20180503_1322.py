# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-03 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0008_auto_20180503_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='calculation_category',
            field=models.CharField(blank=True, choices=[('dry_mixture', '\u0421\u0443\u0445\u0430\u044f \u0441\u043c\u0435\u0441\u044c'), ('ceiling', '\u041f\u043e\u0442\u043e\u043b\u043e\u043a')], max_length=255, null=True, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0434\u043b\u044f \u043a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440\u0430'),
        ),
        migrations.DeleteModel(
            name='CalculationCategory',
        ),
    ]
