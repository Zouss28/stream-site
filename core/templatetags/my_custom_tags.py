from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@register.filter
def increment(value, arg):
    return value + arg

@register.filter
def decrement(value, arg):
    return value - arg