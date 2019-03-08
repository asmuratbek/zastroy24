# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20170903_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('value', models.CharField(max_length=1000, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0441\u0432\u043e\u0439\u0441\u0442\u0432\u043e',
                'verbose_name_plural': '\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u043e \u0442\u043e\u0432\u0430\u0440\u0430',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='props',
            field=models.ManyToManyField(blank=True, to='product.ProductProperty', verbose_name='\u0421\u0432\u043e\u0439\u0441\u0442\u0432\u0430 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430'),
        ),
    ]