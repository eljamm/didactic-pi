from django import template
from django.template.defaultfilters import title as default_title
from .range_iterator import make_list

register = template.Library()


@register.filter(is_safe=True)
def better_title(name: str):
    title = {
        "dht11": "DHT11",
        "8x8matrix": "LED Matrix 8x8",
        "lcd": "LCD",
        "7segment": "Seven Segment Display",
        "ledarray": "LED Array",
        "dpad": "D-Pad",
    }

    if name in title:
        return title[name]
    else:
        return default_title(name)


@register.inclusion_tag('sensor/blocks/extra.html', takes_context=True)
def show_extras(context, extras):
    extra_list = make_list(extras)
    return {
        'sensor_name': context['sensor_name'],
        'extra_list': extra_list
    }
