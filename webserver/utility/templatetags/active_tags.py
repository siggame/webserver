import re
from django import template
from django.template import Context, Template
from django.core.urlresolvers import resolve, Resolver404


register = template.Library()


@register.simple_tag(takes_context=True)
def active_re(context, pattern, *classes):
    classes = classes or ['active']
    request = context['request']
    template = Template(pattern)
    context = Context(context)

    if re.search(template.render(context), request.path):
        return ' '.join(classes)
    return ''


@register.simple_tag(takes_context=True)
def active(context, url_name, *classes):
    classes = classes or ['active']
    request = context['request']

    try:
        resolved = resolve(request.get_full_path())
    except Resolver404:
        return ""

    if resolved.url_name == url_name:
        return ' '.join(classes)
    return ''
