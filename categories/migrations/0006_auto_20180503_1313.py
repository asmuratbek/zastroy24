# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-03 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20180503_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculationcategory',
            name='title',
            field=models.CharField(choices=[('dry_mixture', '\u0421\u0443\u0445\u0430\u044f \u0441\u043c\u0435\u0441\u044c'), ('ceiling', '\u041f\u043e\u0442\u043e\u043b\u043e\u043a')], max_length=255, unique=True),
        ),
    ]
