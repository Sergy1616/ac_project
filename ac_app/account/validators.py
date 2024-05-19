from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    size_MB = filesize / 1024 / 1024
    if size_MB > 5:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
