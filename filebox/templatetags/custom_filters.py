from django import template
import os

register = template.Library()

# @register.filter
# def file_extension(value):
#     return value.name.split('.')[-1].lower()


@register.filter
def file_extension(value):
    return os.path.splitext(value.name)[1][1:].lower()

