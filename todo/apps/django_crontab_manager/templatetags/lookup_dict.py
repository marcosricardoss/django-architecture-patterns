from django import template

register = template.Library()

@register.filter(name='lookup_dict') # pragma: no cover
def my_lookup_dict(mydict, key):
    return mydict[key]
