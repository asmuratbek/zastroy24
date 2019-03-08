# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 02:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_productsearchresults'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductSearchResults',
        ),
        migrations.AddField(
            model_name='product',
            name='found_case',
            field=models.TextField(blank=True, null=True, verbose_name='\u0421\u043b\u0443\u0447\u0430\u0439 \u0435\u0441\u043b\u0438 \u0442\u043e\u0432\u0430\u0440 \u0435\u0441\u0442\u044c \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'),
        ),
        migrations.AddField(
            model_name='product',
            name='not_found_case',
            field=models.TextField(blank=True, help_text='\n            \u0417\u0434\u0435\u0441\u044c \u0434\u043e\u043b\u0436\u043d\u044b \u0431\u044b\u0442\u044c \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435, \u043a\u043e\u0442\u043e\u0440\u043e\u0435 \u0431\u0443\u0434\u0435\u0442 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c\u0441\u044f \u043f\u0440\u0438 \u0432\u044b\u0431\u043e\u0440\u0435 \u0442\u043e\u0439 \u0438\u043b\u0438 \u0438\u043d\u043e\u0439 \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0434\u043b\u044f \u0442\u043e\u0432\u0430\u0440\u0430<br>\n            \u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0442\u0438\u043f\u0430 \u0426\u0432\u0435\u0442 \u0438\u043b\u0438 \u0420\u0430\u0437\u043c\u0435\u0440!<br>\n            \u041f\u0440\u0438 \u0432\u044b\u0431\u043e\u0440\u0435 \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438\u0439 \u043a\u043e\u043c\u0431\u0438\u043d\u0430\u0446\u0438\u044f \u0431\u0443\u0434\u0435\u0442 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0430 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440. <br>\n            \u041e\u0441\u043d\u043e\u0432\u0430\u044f\u0441\u044c \u043d\u0430 \u0432\u044b\u0441\u043b\u0430\u043d\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445 \u0441\u0435\u0440\u0432\u0438\u0441 \u0431\u0443\u0434\u0435\u0442 \u0438\u0441\u043a\u0430\u0442\u044c \u0432 \u0431\u0430\u0437\u0435 \u0442\u043e\u0432\u0430\u0440, \u0438 \u044d\u0442\u043e \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435, \u043a\u043e\u0442\u043e\u0440\u043e\u0435 \u0432\u044b \u0432\u0432\u0435\u0434\u0451\u0442\u0435, \u0431\u0443\u0434\u0435\u0442<br>\n            \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c\u0441\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c. \u0415\u0441\u043b\u0438 \u0432\u044b \u043d\u0435 \u0432\u0432\u0435\u0434\u0451\u0442\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u0442\u043e \u0431\u0443\u0434\u0443\u0442 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u043d\u044b \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0435 \u0444\u0440\u0430\u0437\u044b\n            ', null=True, verbose_name='\u0421\u043b\u0443\u0447\u0430\u0439 \u0435\u0441\u043b\u0438 \u0442\u043e\u0432\u0430\u0440\u0430 \u043d\u0435\u0442 \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'),
        ),
    ]