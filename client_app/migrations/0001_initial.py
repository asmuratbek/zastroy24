# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 14:58
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041e \u043d\u0430\u0441')),
            ],
            options={
                'verbose_name': '\u041e \u043d\u0430\u0441',
                'verbose_name_plural': '\u041e \u043d\u0430\u0441',
            },
        ),
        migrations.CreateModel(
            name='AdminEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='\u041f\u043e\u0447\u0442\u0430')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439?')),
            ],
            options={
                'verbose_name': '\u043f\u043e\u0447\u0442\u0443',
                'verbose_name_plural': '\u041f\u043e\u0447\u0442\u0430 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='AGB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name_plural': '\u0423\u0441\u043b\u043e\u0432\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u0441\u0430\u0439\u0442\u043e\u043c',
            },
        ),
        migrations.CreateModel(
            name='Datenschutz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name_plural': '\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 \u043a\u043e\u043d\u0444\u0438\u0434\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0438',
            },
        ),
        migrations.CreateModel(
            name='DeliveryAndPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name': '\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0438 \u043e\u043f\u043b\u0430\u0442\u0430\u043d\u0430',
                'verbose_name_plural': '\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0438 \u043e\u043f\u043b\u0430\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441')),
                ('answer', models.CharField(max_length=255, verbose_name='\u041e\u0442\u0432\u0435\u0442')),
            ],
            options={
                'verbose_name': '\u0432\u043e\u043f\u0440\u043e\u0441',
                'verbose_name_plural': 'FAQ',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e?')),
                ('name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f')),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
                ('message', models.TextField(max_length=10000, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u043f\u0438\u0441\u043c\u043e',
                'verbose_name_plural': '\u041e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c',
            },
        ),
        migrations.CreateModel(
            name='HowToOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442')),
            ],
            options={
                'verbose_name': '\u043a\u0430\u043a \u0441\u0434\u0435\u043b\u0430\u0442\u044c \u0437\u0430\u043a\u0430\u0437?',
                'verbose_name_plural': '\u041a\u0430\u043a \u0441\u0434\u0435\u043b\u0430\u0442\u044c \u0437\u0430\u043a\u0430\u0437?',
            },
        ),
        migrations.CreateModel(
            name='Impressum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442')),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slider/', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('link', models.URLField(blank=True, max_length=255, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439?')),
            ],
            options={
                'verbose_name': '\u0441\u043b\u0430\u0439\u0434',
                'verbose_name_plural': '\u0421\u043b\u0430\u0439\u0434\u0435\u0440',
            },
        ),
    ]
