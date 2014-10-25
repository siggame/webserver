import re
from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    print pattern
    request = context['request']
    if re.search(pattern, request.path):
        return 'active'
    return ''
