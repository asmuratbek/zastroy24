import os

from django import template
from HTMLParser import HTMLParser

register = template.Library()



@register.filter
def get_wt_image_url(image):
    f, e = os.path.splitext(image.path)
    wt_image = '%s.wt%s' % (f, e)
    if os.path.isfile(wt_image):
        b, s = os.path.splitext(image.url)
        return '%s.wt%s' % (b, s)
    return image.url


@register.filter
def normalize_ck(value):
    new_value = value.replace(r'<pre>(.+?)</pre>', '<p>$1</p>')
    return new_value
