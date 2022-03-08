from atexit import register
from unittest import result
from django import template

register= template.Library()
@register.filter(name='subtraction')
def subtraction(competitor, topper):
    result= topper-competitor
    return result