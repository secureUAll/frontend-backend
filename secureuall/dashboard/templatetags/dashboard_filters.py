from django import template

register = template.Library()


@register.filter
def get_choices(instance, field_name):
    """
    Allows to get choices for object attribute with that field
    -- Example
    Attribute in models.py: riskLevel = models.CharField(max_length=1, choices=riskLevelsOps)
    Usage on template: {{ obj|get_choices:"riskLevel" }}
    Returns: riskLevelsOps
    """
    # Based on https://stackoverflow.com/a/48734571/10735382
    return instance._meta.get_field(field_name).choices


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)