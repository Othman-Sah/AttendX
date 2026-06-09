import hashlib

from django import template


register = template.Library()


@register.filter
def get_item(mapping, key):
    return mapping.get(key)


@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """Divides the value by the argument."""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def file_version(file_field):
    """Return a stable cache-busting token for an uploaded file."""
    if not file_field:
        return ''

    try:
        name = file_field.name or ''
        size = getattr(file_field, 'size', 0)
        modified = file_field.storage.get_modified_time(name).timestamp()
        raw_value = f'{name}:{size}:{modified}'
    except Exception:
        raw_value = getattr(file_field, 'name', '') or ''

    return hashlib.md5(raw_value.encode('utf-8')).hexdigest()[:12]
