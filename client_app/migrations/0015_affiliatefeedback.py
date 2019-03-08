# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-25 02:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0014_auto_20171224_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e?')),
                ('first_name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f')),
                ('last_name', models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('phone_number', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('affiliate', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='client_app.Contact', verbose_name='\u0424\u0438\u043b\u0438\u0430\u043b')),
            ],
        ),
    ]