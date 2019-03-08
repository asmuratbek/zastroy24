import json
import os

from django.core.mail import EmailMessage
from django.forms import model_to_dict

from categories.models import Category, Brand
from MyBrands import settings
from client_app.forms import FeedbackForm
from client_app.models import About, Contact, SiteSettings
from order.utils import get_basket_count, get_basket, get_comparable


def generate_view_params(request):
    meta_description = open(os.path.join(settings.BASE_DIR, 'Meta', 'description.txt'), 'r')
    d = ' '.join(line for line in meta_description)
    meta_description.close()

    meta_keywords = open(os.path.join(settings.BASE_DIR, 'Meta', 'keywords.txt'), 'r')
    kw = ' '.join(line for line in meta_keywords)
    meta_keywords.close()

    categories = []
    for category in Category.objects.filter(is_active=True, parent_category=None).order_by('id'):
        _item = model_to_dict(category)
        _item['sub_categories'] = []
        for sub_category in Category.objects.filter(parent_category=category, is_active=True).order_by('id'):
            _sub_item = model_to_dict(sub_category)
            _sub_item['sub_categories'] = []
            for _sub_category in Category.objects.filter(parent_category=sub_category, is_active=True).order_by('id'):
                _sub_item['sub_categories'].append(_sub_category)

            _item['sub_categories'].append(_sub_item)
        categories.append(_item)

    site_setting = SiteSettings.objects.first()

    params = {
        'meta_description': d,
        'meta_keywords': kw,
        'categories': categories,
        'basket_count': get_basket_count(request),
        'abstract_basket': get_basket(request.COOKIES),
        'site_setting': site_setting,
        'comparable_count': len(get_comparable(request.COOKIES)),
        'comparable': get_comparable(request.COOKIES),
        'abstract_feedback_form': FeedbackForm(request.POST)
    }
    return params


def send_email_notification(title, body, to):
    email = EmailMessage(title, body=body, to=to)
    email.content_subtype = 'html'
    email.send()


def get_weight_property_object():
    _settings = SiteSettings.objects.first()
    if _settings:
        return _settings.weight.id
    return None
