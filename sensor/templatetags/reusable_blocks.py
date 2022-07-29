from django import template
from .range_iterator import make_list

register = template.Library()


@register.inclusion_tag('sensor/blocks/extra.html', takes_context=True)
def show_extras(context, extras):
    extra_list = make_list(extras)
    return {
        'sensor_name': context['sensor_name'],
        'extra_list': extra_list
    }
