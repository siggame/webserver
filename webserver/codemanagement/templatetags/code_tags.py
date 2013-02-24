from django import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()


@register.filter
@stringfilter
def clean_repo_name(value):
    return re.sub(r'__\d+\.git$', '.git', value)
