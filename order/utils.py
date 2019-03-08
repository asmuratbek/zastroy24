import json

from django.core.exceptions import ObjectDoesNotExist

from MyBrands import settings
from product.models import Product


def splice_row(basket, _id):
    return [row for row in basket if int(row['id']) != int(_id)]


def splice(object, item):
    return [row for row in object if row != item]


def is_in_basket(request, product_id):
    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
        result = False
        for data in cookie_data:
            if int(data['product_id']) == int(product_id):
                result = True
                break
        return result
    return False


def get_basket_count(request):
    if settings.BASKET_COOKIE_NAME in request.COOKIES:
        cookie_data = json.loads(request.COOKIES[settings.BASKET_COOKIE_NAME])
        return len(cookie_data)
    return 0


def get_basket(cookies):
    if settings.BASKET_COOKIE_NAME in cookies:
        cookie_data = json.loads(cookies[settings.BASKET_COOKIE_NAME])
    else:
        cookie_data = []

    prepared_objects = []
    for row in cookie_data:
        try:
            product = Product.objects.get(id=int(row['product_id']))
        except ObjectDoesNotExist:
            cookie_data = splice_row(cookie_data, row['id'])
            continue

        prepared_objects.append({
            'product_id': int(product.id),
            'basket_id': int(row['id']),
            'count': int(row['count'])
        })

    return prepared_objects


def get_comparable(cookies):
    if settings.COMPARISON_COOKIE_NAME in cookies:
        cookie_data = json.loads(cookies[settings.COMPARISON_COOKIE_NAME])
        return cookie_data
    return []


def contains(array, element, field=None):
    #print array, element, field
    if field:
        for item in array:
            if isinstance(array, object):
                if item.key.__dict__[field] == element:
                    return True
            elif isinstance(array, dict):
                if item['key'][field] == element:
                    return True
    else:
        for item in array:
            if item == element:
                return True
    return False
