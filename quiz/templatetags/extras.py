from django import template
register = template.Library()

@register.filter
def get_item(d, key):
    """
    Usage in template: {{ my_dict|get_item:"some_key" }}
    """
    if isinstance(d, dict):
        return d.get(key, "")
    return ""