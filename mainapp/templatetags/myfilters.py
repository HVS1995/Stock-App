from django import template
register = template.Library()

@register.filter
def get(mapping, key):                      #mapping is a type of dictionary
    return mapping.get(key, '')     