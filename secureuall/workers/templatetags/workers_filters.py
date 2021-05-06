from django import template

register = template.Library()


@register.filter
def color(value):
    """Removes all values of arg from the given string"""
    if value.lower() in ['active']:
        return 'primary'
    if value.lower() in ['down']:
        return 'danger'

    return 'dark'

