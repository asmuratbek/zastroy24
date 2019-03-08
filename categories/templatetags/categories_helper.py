from django import template

register = template.Library()


@register.filter
def brands_len(value):
    if isinstance(value, list):
        return len(value)
    return 0


@register.simple_tag
def angular_render(value):
    return value


@register.filter
def to_number(value):
    value = str(value)
    return float(''.join(i for i in value if i.isdigit()))
