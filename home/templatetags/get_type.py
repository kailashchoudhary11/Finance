from atexit import register
from django import template

register = template.Library()

@register.filter
def typededo(value):
    return type(value)

@register.filter
def usd(value):
    return f"${value:,}"