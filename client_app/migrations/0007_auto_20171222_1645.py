# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-22 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0006_auto_20171222_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name': '\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430', 'verbose_name_plural': '\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430'},
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='message',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='feedback',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f'),
        ),
    ]
