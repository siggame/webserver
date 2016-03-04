from django import template
from django.template.defaultfilters import stringfilter
from django.core.cache import cache

from ..models import TeamSubmission

import re

register = template.Library()


@register.filter
@stringfilter
def clean_repo_name(value):
    return re.sub(r'__\d+\.git$', '.git', value)


@register.filter
@stringfilter
def tag_from_hash(commit_hash):
    cache_key = "git-tag" + commit_hash
    tag = cache.get(cache_key)

    if tag is not None:
        return commit_hash

    try:
        submission = TeamSubmission.objects.get(commit=commit_hash)
        cache.set(cache_key, submission.name, 30)
    except TeamSubmission.DoesNotExist:
        cache.set(cache_key, commit_hash, 30)
        tag = commit_hash

    return tag
