from django import template

register = template.Library()

@register.simple_tag
def iterate_over(n):
    return range(n)