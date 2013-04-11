from django.core.validators import RegexValidator

sha1_validator = RegexValidator(regex="^[a-f0-9]{40}$",
                                message="Must be valid sha1 sum")
tag_validator = RegexValidator(regex="^[A-Za-z][\w\-\.]+[A-Za-z]$",
                               message="Must be letters and numbers" +
                               " separated by dashes, dots, or underscores")
