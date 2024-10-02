from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def d_url(url_name, *args, **kwargs):
    """ Dynamic url maker filter """
    return reverse(url_name, args=args, kwargs=kwargs)
