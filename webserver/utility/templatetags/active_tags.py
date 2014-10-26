import re
from django import template
from django.conf import settings
from django.template import Context, Template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    request = context['request']
    template = Template(pattern)
    context = Context(context)

    if re.search(template.render(context), request.path):
        return 'active'
    return ''
