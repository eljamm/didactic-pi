from django import template

register = template.Library()


@register.simple_tag
def iterate_over(n: int) -> range:
    return range(n)


@register.simple_tag
def make_list(extras: str) -> list:
    list = extras.split(", ")
    return list
