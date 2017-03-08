from django import template

register = template.Library()


@register.filter("remove_key")
def remove_key(value, arg):
    return value.split(arg)[0]