# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(help_text='\u041d\u0443\u0436\u0435\u043d \u0434\u043b\u044f URL', max_length=255, verbose_name='slug')),
                ('description', models.TextField(blank=True, help_text='\u041d\u0443\u0436\u0435\u043d \u0434\u043b\u044f SEO', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0431\u0440\u0435\u043d\u0434\u0430')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430')),
                ('is_show', models.BooleanField(default=True, verbose_name='\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435?')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439?')),
            ],
            options={
                'verbose_name': '\u0411\u0440\u0435\u043d\u0434',
                'verbose_name_plural': '\u0411\u0440\u0435\u043d\u0434\u044b',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.CharField(help_text='\u041d\u0443\u0436\u0435\u043d \u0434\u043b\u044f URL', max_length=255, verbose_name='slug')),
                ('description', models.TextField(blank=True, help_text='\u041d\u0443\u0436\u0435\u043d \u0434\u043b\u044f SEO', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439?')),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f',
                'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438',
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f'),
        ),
    ]