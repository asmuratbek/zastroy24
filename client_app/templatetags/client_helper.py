from HTMLParser import HTMLParser

from django import template

register = template.Library()


class MTStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

@register.filter
def length(value):
    if isinstance(value, (int, float)):
        return 0
    return len(value)

@register.filter
def clean_html(value):
    if value:
        s = MTStripper()
        s.feed(value)
        return s.get_data()
    return value