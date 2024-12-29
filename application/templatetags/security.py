from django import template

register = template.Library()

@register.filter
def username_security(value):
    """Mask all characters except the first."""
    if len(value) <= 1:
        return '*'
    return value[0] + '*' * (len(value) - 1)