# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import threading
from random import randint

import operator
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from slugify import slugify
from django.views.decorators.http import require_POST

from MyBrands import settings
from categories.models import Category, Brand
from client_app.models import Slider, AdminEmails
from client_app.utils import generate_view_params, get_weight_property_object, send_email_notification
from order.models import Order, OrderRow
from order.utils import is_in_basket
from product.utils import set_cookie
from .models import Product, ProductImage, ProductProperty, AllProductProperties
from .forms import OrderInOneClickForm, CalculationForm


# Create your views here.


def product_single(request, product_slug):
    try:
        product = Product.objects.get(slug=product_slug)
    except:
        raise Http404

    suggested_products = Product.objects.filter(is_active=True, category=product.category).exclude(id=product.id)

    params = {
        'product': product,
        'suggested_products': suggested_products,
        'form': OrderInOneClickForm()
    }
    params.update(generate_view_params(request))
    return render(request, 'app/product-single.html', params)


def calculator(request):
    try:
        _cat = Category.objects.get(slug='gipsokartonnye-sistemy')
    except:
        _cat = None

    second_categories = Category.objects.filter(parent_category=_cat)
    second_products = Product.objects.filter(category_id__in=[x.id for x in second_categories])
    calculation_form = CalculationForm()

    params = {
        'second_categories': second_categories,
        'second_products': second_products,
        'products': Product.objects.all(),
        'calculation_form': calculation_form,
    }
    params.update(generate_view_params(request))
    return render(request, 'app/calculator.html', params)


def load_products(request):
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id).order_by('title')
    return render(request, 'app/product_dropdown_form.html', {'products': products})


def calculation(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        area = request.POST.get('area')
        thickness = request.POST.get('thickness')
        product = Product.objects.get(id=product)

        consumption = (float(thickness) / 1000) * float(area) * product.consumption
        quantity_int = int(consumption / product.weight)
        quantity_round = round(consumption / product.weight)

        if quantity_int == quantity_round:
            quantity = quantity_int + 1
        else:
            quantity = quantity_round

        quantity = int(quantity)

        summ = quantity * product.price

    return render(request, 'app/calculation.html', {'summ': summ, 'quantity': quantity})


def search(request):
    search_word = request.GET.get('search_word')

    result = None
    result_count = 0
    if search_word:
        query_list = search_word.split()
        holder = Product.objects.filter(reduce(operator.and_, (Q(title__icontains=q) for q in query_list)))
        result_count = holder.count()
        pagination = Paginator(holder, 20)
        result = pagination.page(request.GET.get('page', 1))

    params = {
        'search_word': search_word,
        'products': result,
        'result_count': result_count
    }
    params.update(generate_view_params(request))
    return render(request, 'app/search-results.html', params)


@csrf_exempt
def create_product(request):
    article = request.POST.get('article')
    title = request.POST.get('title')
    slug = slugify(title)
    category_id = request.POST.get('category_id')
    description = request.POST.get('description')
    characteristics = json.loads(request.POST.get('characteristics'))
    images = request.FILES.getlist('files')
    price = float(request.POST.get('price'))
    discount = float(request.POST.get('discount'))
    brand_title = request.POST.get('brand')
    documentation = request.POST.get('documentation')

    try:
        p = Product.objects.get(slug=slug)
        return JsonResponse(dict(success=True, message='Product already exists'))
    except ObjectDoesNotExist:
        pass

    try:
        category = Category.objects.get(id=category_id)
    except:
        return JsonResponse(dict(success=False, message='Category not found!'))

    brand = None
    if brand_title:
        try:
            brand = Brand.objects.get(title=brand_title)
        except ObjectDoesNotExist:
            brand = Brand.objects.create(title=brand_title, slug=slugify(brand_title))

    main_image = images[0]

    product = Product(
        article=article,
        title=title,
        slug=slug,
        category=category,
        description=description,
        documentation=documentation,
        price=price,
        discount=discount,
        brand=brand,
        main_image=main_image
    )

    product.save()

    for c in characteristics:
        if '?' in c['key']:
            _key = c['key'].split('?')[0]
        else:
            _key = c['key']
        try:
            prop_key = AllProductProperties.objects.get(title=_key.strip().lower())
        except ObjectDoesNotExist:
            prop_key = AllProductProperties.objects.create(title=_key.strip().lower())
        if slugify(_key.strip()) == slugify('вес брутто'):
            value_holder = c['value'].strip().split()
            ProductProperty.objects.create(product=product, key=prop_key,
                                           value=float(value_holder[0].replace(',', '.')), value_type=value_holder[1])
        else:
            if '?' in c['key']:
                ProductProperty.objects.create(product=product, key=prop_key, value=c['value'],
                                               prop_tip=c['key'].strip().split('?')[1])
            else:
                ProductProperty.objects.create(product=product, key=prop_key, value=c['value'])

    for img in images:
        ProductImage.objects.create(product=product, image=img)

    with open('/var/www/html/fixstroy_python/parser_log.log', 'w') as file:
        file.write('Last uploaded product: %s, category: %s' % (product.slug, category.title))
        file.close()

    return JsonResponse(dict(success=True, message='Successfully added product'))


def buy_on_one_click(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    form = OrderInOneClickForm(request.POST)
    if form.is_valid():
        order = Order()
        order.email = form.cleaned_data['email']
        order.address = ""
        order.name = form.cleaned_data['name']
        order.comment = form.cleaned_data['comment']
        order.phone = form.cleaned_data['phone']
        product_weight = product.property.filter(key_id=get_weight_property_object()).first()
        order.total_weight = float(product_weight.value) * int(form.cleaned_data['count'])
        order.save(force_insert=True)
        item = OrderRow.objects.create(product=product, count=form.cleaned_data['count'])
        order.order_items.add(item)

        template = loader.get_template('app/email/order.html')
        protocol = 'https://' if request.is_secure() else 'http://'
        context = {
            'link': protocol + request.get_host() + reverse(
                'admin:order_order_change',
                args=(order.id,)
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

        return JsonResponse(dict(success=True, message='Заказ оформлен'))

    return JsonResponse(dict(success=False, message=str(form.errors)))


def calculate_ceiling(request):
    category_id = request.POST.get('category_id')
    product_id = request.POST.get('product_id')

    value = request.POST.get('value')

    if category_id:
        category = Category.objects.get(id=category_id)
    else:
        category = None

    if product_id:
        product = Product.objects.get(id=product_id)
    else:
        product = None

    filters = dict()

    _cat = Category.objects.get(slug='gipsokartonnye-sistemy')

    if category:
        filters['category'] = category
    else:
        filters['category_id__in'] = [x.id for x in Category.objects.filter(parent_category=_cat)]

    result = None

    if product:
        result = value / product.consumption
