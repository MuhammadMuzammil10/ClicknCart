from django import template  
register = template.Library()
from django.template.defaultfilters import  floatformat 
from django.contrib.humanize.templatetags.humanize import intcomma

@register.filter
def format_price(value):
    value = int(value)
    if value < 100:
        return '{}'.format(value)
    elif value < 1000:
        return '{}'.format(floatformat(value, 2))
    else:
        return '{}'.format(intcomma(floatformat(value, 2)))

# @register.filter(name='replace_hyphen')
# def replace_hyphen(value):
#     return value.replace('-' , ' ')
