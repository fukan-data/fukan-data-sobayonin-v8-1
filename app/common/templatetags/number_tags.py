from django import template

register = template.Library()


@register.simple_tag
def intcomma(num: int) -> str:
    if isinstance(num, int):
        return '{:,}'.format(num)
    else:
        return ''


@register.filter
def to_remainder(num, base):
    return num % base
