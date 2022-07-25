from django import template

register = template.Library()


@register.simple_tag
def iterate_over(n: int) -> range:
    return range(n)


@register.simple_tag
def make_list(extra: str) -> list:
    list = extra.split(", ")
    return list
