# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-25 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0015_affiliatefeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliatefeedback',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438'),
        ),
    ]
