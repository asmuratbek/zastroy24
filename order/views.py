# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import threading
from openpyxl import Workbook, load_workbook

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from MyBrands import settings
from client_app.models import AdminEmails
from client_app.utils import generate_view_params, get_weight_property_object, send_email_notification
from order.forms import CheckoutForm
from order.models import Order, OrderRow
from order.utils import splice_row, splice, contains
from product.models import Product
from product.utils import set_cookie


# Create your views here.


def add_to_basket(request, p_slug):
    if request.is_ajax():
        try:
            product = Product.objects.get(slug=p_slug)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, messagae='Товар не найден'))

        if settings.BASKET_COOKIE_NAME in request.COOKIES:
            cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
        else:
            cookie_data = []

        last_item_id = cookie_data[len(cookie_data) - 1]['id'] if len(cookie_data) > 0 else 0

        count = request.POST.get('count', 1)

        already_have = False
        for _item in cookie_data:
            if _item['product_id'] == product.id:
                already_have = True
                _item['count'] += count
                break

        if not already_have:
            item = {
                'product_id': product.id,
                'count': count,
                'id': last_item_id + 1
            }
            cookie_data.append(item)

        response = JsonResponse(dict(
            success=True,
            message='Товар добавлен в корзину' if not already_have else 'Количество товара обновлено',
            is_new=not already_have
        ))
        return set_cookie(response, settings.BASKET_COOKIE_NAME, json.dumps(cookie_data))
    return JsonResponse(dict(success=False, message='Запрос должен быть POST'))


def clean_basket(request):
    response = JsonResponse(dict(
        success=True,
        message='Корзина отчищена'
    ))
    return set_cookie(response, settings.BASKET_COOKIE_NAME, json.dumps([]))


def update_quantity_of_basket_item(request, b_id):

    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
    else:
        cookie_data = []

    response = JsonResponse(dict(
        success=False,
        message='Товар не найден'
    ))

    for i in range(0, len(cookie_data)):
        c_data = cookie_data[i]

        if int(c_data['id']) == int(b_id):
            count = request.POST.get('count')
            c_data['count'] = int(count)
            cookie_data[i] = c_data
            response = JsonResponse(dict(
                success=True,
                message='Количество товара обновлено'
            ))

    return set_cookie(response, settings.BASKET_COOKIE_NAME, json.dumps(cookie_data))


def remove_from_basket(request, b_id):
    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
    else:
        cookie_data = []

    new_cookie_data = []
    for r in cookie_data:
        if int(r['id']) != int(b_id):
            new_cookie_data.append(r)

    response = JsonResponse(dict(success=True, message='Товар убран с корзины'))
    return set_cookie(response, settings.BASKET_COOKIE_NAME, json.dumps(new_cookie_data))


def list_basket(request):
    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
    else:
        cookie_data = []

    prepared_objects = []
    total_price = 0
    total_weight = 0
    for row in cookie_data:
        try:
            product = Product.objects.get(id=int(row['product_id']))
        except ObjectDoesNotExist:
            cookie_data = splice_row(cookie_data, row['id'])
            continue
        product_weight = product.property.filter(key_id=get_weight_property_object()).first()
        item = {
            'product': product,
            'count': row['count'],
            'row_price': product.get_price() * int(row['count']),
            'id': row['id']
        }
        total_price += item['row_price']
        if product_weight:
            total_weight += float(product_weight.value) * int(row['count'])
        prepared_objects.append(item)

    params = {
        'basket': prepared_objects,
        'total_price': total_price,
        'product_count': len(prepared_objects),
        'total_weight': total_weight
    }
    params.update(generate_view_params(request))
    return render(request, 'app/basket.html', params)


def get_total_basket_price(request):
    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
    else:
        cookie_data = []

    total_price = 0
    total_weight = 0
    for row in cookie_data:
        try:
            product = Product.objects.get(id=int(row['product_id']))
        except ObjectDoesNotExist:
            cookie_data = splice_row(cookie_data, row['id'])
            continue
        total_price += product.get_price() * int(row['count'])
        product_weight = product.property.filter(key_id=get_weight_property_object()).first()
        if product_weight:
            total_weight += float(product_weight.value) * int(row['count'])

    return JsonResponse(dict(
        total_price=total_price,
        product_count=len(cookie_data),
        total_weight=total_weight
    ))


def add_to_comparison(request, p_slug):
    try:
        product = Product.objects.get(slug=p_slug)
    except:
        raise Http404

    if settings.COMPARISON_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.COMPARISON_COOKIE_NAME])
    else:
        cookie_data = []

    if int(product.id) not in cookie_data:
        cookie_data.append(product.id)
        response = JsonResponse(dict(
            success=True,
            message='У вас %s товаров к сравнению' % str(len(cookie_data)),
            mode='add',
            count=len(cookie_data)
        ))
    else:
        cookie_data = [int(x) for x in cookie_data if int(x) != int(product.id)]
        response = JsonResponse(dict(
            success=True,
            message='Товар убран с сравнения. У вас %s товаров к сравнению' % str(len(cookie_data)),
            mode='remove',
            count=len(cookie_data)
        ))

    return set_cookie(response, settings.COMPARISON_COOKIE_NAME, json.dumps(cookie_data))


def list_of_comparison(request):
    if settings.COMPARISON_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.COMPARISON_COOKIE_NAME])
    else:
        cookie_data = []

    prepared_products = list()
    comparable_properties = list()
    for item in cookie_data:
        try:
            product = Product.objects.get(id=int(item))
        except:
            cookie_data = splice(cookie_data, item)
            continue

        prepared_products.append(product)
        for property in product.property.all():
            if not contains(comparable_properties, property.key.id, field='id'):
                comparable_properties.append(property)

    params = {
        'products': prepared_products,
        'properties': comparable_properties
    }
    params.update(generate_view_params(request))
    return render(request, 'app/comparison.html', params)


def checkout(request):
    form = CheckoutForm(request.POST)
    params = {
        'form': form
    }
    if request.POST:
        if form.is_valid():
            if settings.BASKET_COOKIE_NAME in request.COOKIES:
                cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])

                order_object = Order(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address']
                )
                order_object.save()

                total_weight = 0
                for item in cookie_data:
                    try:
                        product = Product.objects.get(id=int(item['product_id']))
                    except ObjectDoesNotExist:
                        cookie_data = splice_row(cookie_data, item['id'])
                        continue
                    total_weight += (float(product.property.filter(key_id=get_weight_property_object()).first().value) * int(item['count']))
                    order_item = OrderRow.objects.create(
                        product=product,
                        count=int(item['count'])
                    )
                    order_object.order_items.add(order_item)

                order_object.total_weight = total_weight
                
                order_object.save()

                # отсюда и до save создание файла excel отчёта

                workbook = Workbook()
                sheet = workbook.active
                sheet.title = "Заказ"

                sheet.append(['Артикул', 'Название', 'Категория', 'Количество', 'Цена', 'Стоимость'])
                
                for item in order_object.order_items.all():
                    sheet.append([item.product.article, item.product.title, item.product.category.title, item.count, item.product.get_price(), item.count*item.product.get_price()])

                sheet.append(['', '', '', '', 'Общая стоимость:', order_object.get_order_full_price()])

                excel_file = 'order/' + str(order_object.id) + '.xlsx'

                workbook.save(settings.MEDIA_ROOT + excel_file)

                order_object.excel_file = excel_file

                order_object.save()


                template = loader.get_template('app/email/order.html')
                protocol = 'https://' if request.is_secure() else 'http://'
                context = {
                    'link': protocol + request.get_host() + reverse(
                        'admin:order_order_change',
                        args=(order_object.id,)
                    )
                }
                mail_body = template.render(context, request)

                thread = threading.Thread(
                    target=send_email_notification,
                    args=(
                        'Новый заказ | Vesta Stroy',
                        mail_body,
                        [x.email for x in AdminEmails.objects.all()]
                    )
                )
                thread.start()

                params['success'] = True

            else:
                params['success'] = False
                params['error'] = 'Вы не добавили товаров в карзину'
        else:
            params['success'] = False
            params['error'] = str(form.errors)



    params.update(generate_view_params(request))
    return render(request, 'app/paypal.html', params)
