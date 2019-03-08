import os

from django import template

register = template.Library()



@register.filter
def calculate_discount(value, discount):
    if isinstance(value, (str, unicode)):
        return value

    if isinstance(discount, (str, unicode)):
        return value

    if discount <= 0 or value <= 0:
        return value

    percent = int(discount)
    full_price = int(value)
    result = (full_price * percent) / 100
    return value - result


@register.filter
def get_wt_image_url(image):
    f, e = os.path.splitext(image.path)
    wt_image = '%s.wt%s' % (f, e)
    if os.path.isfile(wt_image):
        b, s = os.path.splitext(image.url)
        return '%s.wt%s' % (b, s)
    return image.url


@register.filter
def array_reversed(obj):
    return reversed(obj)


@register.simple_tag
def show_link(page, num_pages, current_page):
    page = int(page)
    num_pages = int(num_pages)
    current_page = int(current_page)

    if page == current_page:
        return True
    if (page <= 5 and current_page <= 5) or (page >= num_pages - 5 and current_page >= num_pages - 5):
        return True

    if page == 1 or page == num_pages:
        return True

    if current_page - page in [1, 2] or page - current_page in [1, 2]:
        return True

    return False

@register.assignment_tag
def set(value):
    return value


@register.simple_tag
def get_prepared_url(path, param):
    if '?' in path:
        _url = path.split('?')[0]
        _params = path.split('?')[1]

        if '&' in _params:
            _params = _params.split('&')
            prepared_params = []
            for item in _params:
                key = item.split('=')[0]
                value = item.split('=')[1]
                prepared_params.append({'key': key, 'value': value})

            _params = prepared_params
        elif '=' in _params:
            _params = [{
                'key': _params.split('=')[0],
                'value': _params.split('=')[1]
            }]
        else:
            _params = []

        parameter_index = -1
        for x in range(0, len(_params)):
            if _params[x]['key'] == param:
                parameter_index = x
                break

        if parameter_index > -1:
            _params.remove(_params[parameter_index])

        if len(_params) > 0:
            args = '&'.join("%s=%s" % (x['key'], x['value']) for x in _params)
            args += '&'
        else:
            args = ''
        return _url + '?' + args
    return path + '?'


@register.filter
def contains(basket, product_id):
    for item in basket:
        if int(item['product_id']) == int(product_id):
            return True
    return False


@register.filter
def get_basket_id(basket, product_id):
    for item in basket:
        if int(item['product_id']) == int(product_id):
            return int(item['basket_id'])
    return False


@register.filter
def get_basket_item(basket, product_id):
    for item in basket:
        if int(item['product_id']) == int(product_id):
            return item
    return None
