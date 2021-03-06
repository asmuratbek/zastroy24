# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-24 14:40
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0019_auto_20171224_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438')),
                ('expires_date', models.DateField(blank=True, null=True, verbose_name='\u0427\u0438\u0441\u043b\u043e \u0434\u043e \u043a\u043e\u0442\u043e\u0440\u043e\u0433\u043e \u0431\u0443\u0434\u0435\u0442 \u0434\u0435\u0439\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c \u0430\u043a\u0446\u0438\u044f')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='\u0422\u043e\u0432\u0430\u0440 \u043d\u0430 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0434\u0435\u0439\u0441\u0442\u0432\u0443\u0435\u0442 \u0430\u043a\u0446\u0438\u044f')),
            ],
            options={
                'verbose_name': ('\u0430\u043a\u0446\u0438\u044e',),
                'verbose_name_plural': '\u0410\u043a\u0446\u0438\u0438',
            },
        ),
    ]
