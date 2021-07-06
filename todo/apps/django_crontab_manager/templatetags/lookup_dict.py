from django import template

register = template.Library()

@register.filter(name='lookup_dict')
def my_lookup_dict(mydict, key):
    return mydict[key]
