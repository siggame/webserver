from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from dulwich.repo import check_ref_format

import re

sha1_validator = RegexValidator(regex="^[a-f0-9]{40}$",
                                message="Must be valid sha1 sum")
tag_regex = re.compile(r'^[\w\-\.]+$')


def tag_validator(value):
    if not tag_regex.match(value):
        msg = "Must be letters and numbers separated "
        msg += "by dashes, dots, or underscores"
        raise ValidationError(msg)
    if not check_ref_format('refs/tags/' + value):
        msg = "Invalid tag. Tags must adhere to ref formats defined here: "
        msg += "https://www.kernel.org/pub/software/scm/git/docs/git-check-ref-format.html"
        raise ValidationError(msg)
