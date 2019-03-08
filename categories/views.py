# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.shortcuts import render, render_to_response
from slugify import slugify
from django.views.decorators.csrf import csrf_exempt

from client_app.utils import generate_view_params
from product.models import Product
from .models import Category, Brand


# Create your views here.


def get_filtering_products(request, filtering_categories, sorting, contains=True):
    min_price = int(float(request.POST.get('min_price')))
    max_price = int(float(request.POST.get('max_price')))

    brand = json.loads(request.POST.get('brands', '[]'))

    filters = dict(
        price__lte=max_price,
        price__gte=min_price,
        is_active=True
    )
    if len(brand) > 1:
        filters['brand_id__in'] = brand
    elif len(brand) == 1:
        filters['brand_id'] = brand[0]

    if contains:
        filters['category__in'] = filtering_categories
    else:
        filters['category'] = filtering_categories

    paginator = Paginator(Product.objects.filter(**filters).order_by(sorting), 20)
    products = paginator.page(request.GET.get('page', 1))

    # print paginator.object_list

    params = {
        'products': products
    }
    params.update(generate_view_params(request))
    return render(request, 'app/partial/products.html', params)


def parent_category(request, category_slug):
    try:
        _category = Category.objects.get(slug=category_slug)
    except:
        raise Http404

    filtering_categories = [_category]
    prepared_category = model_to_dict(_category)
    prepared_category['sub_categories'] = list()
    prepared_category['seo_thumbnail'] = _category.seo_thumbnail
    for sub_cat in Category.objects.filter(parent_category=_category, is_active=True).order_by('id'):
        filtering_categories.append(sub_cat)
        prepared_sub_category = model_to_dict(sub_cat)
        prepared_sub_category['seo_thumbnail'] = sub_cat.seo_thumbnail
        prepared_sub_category['sub_categories'] = list()
        prepared_sub_category['parent_category'] = Category.objects.get(id=prepared_sub_category['parent_category'])
        for _sub_cat in Category.objects.filter(parent_category=sub_cat, is_active=True).order_by('id'):
            filtering_categories.append(_sub_cat)
            prepared_sub_category['sub_categories'].append(_sub_cat)
        prepared_category['sub_categories'].append(prepared_sub_category)

    sorting = request.GET.get('sorting', 'price')
    abstract_products = Product.objects.filter(is_active=True, category__in=filtering_categories).order_by(sorting)
    paginator = Paginator(abstract_products, 20)
    products = paginator.page(request.GET.get('page', 1))

    available_brands = []
    for item in abstract_products:
        if item.brand not in available_brands:
            available_brands.append(item.brand)

    if request.is_ajax():
        return get_filtering_products(request, filtering_categories, sorting)

    params = {
        'category': prepared_category,
        'products': products,
        'level': 'parent',
        'total_product_count': Product.objects.filter(is_active=True, category__in=filtering_categories).count(),
        'sorting': sorting,
        'brands': available_brands,
        'min_price': abstract_products.filter(price__gte=0).order_by('price').first().price if abstract_products else 0,
        'max_price': abstract_products.filter(price__gte=0).order_by('price').last().price if abstract_products else 2000
    }
    #print params
    params.update(generate_view_params(request))
    return render(request, 'app/category.html', params)


def second_level_category(request, category_slug, second_category_slug):
    try:
        _category = Category.objects.get(slug=second_category_slug)
    except:
        raise Http404

    filtering_categories = [_category]
    prepared_category = model_to_dict(_category)
    prepared_category['seo_thumbnail'] = _category.seo_thumbnail
    prepared_category['sub_categories'] = []
    prepared_category['parent_category'] = Category.objects.get(id=prepared_category['parent_category'])
    for sub_cat in Category.objects.filter(is_active=True, parent_category=_category).order_by('id'):
        filtering_categories.append(sub_cat)
        prepared_category['sub_categories'].append(sub_cat)

    sorting = request.GET.get('sorting', 'price')
    abstract_products = Product.objects.filter(is_active=True, category__in=filtering_categories).order_by(sorting)
    paginator = Paginator(abstract_products, 20)
    products = paginator.page(request.GET.get('page', 1))

    available_brands = []
    for item in abstract_products:
        if item.brand not in available_brands:
            available_brands.append(item.brand)

    if request.is_ajax():
        return get_filtering_products(request, filtering_categories, sorting)

    params = {
        'category': prepared_category,
        'products': products,
        'level': 'second',
        'total_product_count': Product.objects.filter(is_active=True, category__in=filtering_categories).count(),
        'sorting': sorting,
        'brands': available_brands,
        'min_price': abstract_products.filter(price__gte=0).order_by('price').first().price if abstract_products else 0,
        'max_price': abstract_products.filter(price__gte=0).order_by('price').last().price if abstract_products else 2000
    }
    params.update(generate_view_params(request))
    return render(request, 'app/category.html', params)


def third_level_category(request, category_slug, second_category_slug, third_category_slug):
    try:
        _category = Category.objects.get(slug=third_category_slug)
    except:
        raise Http404

    display_categories = Category.objects.filter(is_active=True, parent_category=_category.parent_category).all()

    sorting = request.GET.get('sorting', 'price')
    abstract_products = Product.objects.filter(is_active=True, category=_category).order_by(sorting)
    paginator = Paginator(Product.objects.filter(is_active=True, category=_category).order_by(sorting), 20)
    products = paginator.page(request.GET.get('page', 1))

    available_brands = []
    for item in abstract_products:
        if item.brand not in available_brands:
            available_brands.append(item.brand)

    if request.is_ajax():
        return get_filtering_products(request, _category, sorting, contains=False)

    params = {
        'category': _category,
        'products': products,
        'level': 'third',
        'display_categories': display_categories,
        'total_product_count': Product.objects.filter(is_active=True, category=_category).count(),
        'sorting': sorting,
        'brands': available_brands,
        'min_price': abstract_products.filter(price__gte=0).order_by('price').first().price if abstract_products else 0,
        'max_price': abstract_products.filter(price__gte=0).order_by('price').last().price if abstract_products else 2000
    }
    params.update(generate_view_params(request))
    return render(request, 'app/category.html', params)


@csrf_exempt
def create_category(request):
    title = request.POST.get('title')
    _slug = slugify(title)
    parent_id = request.POST.get('parent_id', None)

    try:
        cat = Category.objects.get(slug=_slug)
        return JsonResponse(dict(id=cat.id))
    except ObjectDoesNotExist:
        pass

    #print _slug

    category = Category(
        title=title,
        slug=_slug
    )

    if parent_id:
        parent_cat = Category.objects.get(id=int(parent_id))
        category.parent_category = parent_cat

    category.save()

    return JsonResponse(dict(id=category.id))
