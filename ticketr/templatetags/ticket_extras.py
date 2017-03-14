from django import template

register = template.Library()


@register.filter("remove_key")
def remove_key(value, arg):
    return value.split(arg)[0]


@register.filter("get_fees_total")
def get_fees_total(ticket_price, fee):
    ticket_price = float(ticket_price)
    return ((ticket_price/100 * float(fee)) + 1) + ticket_price

@register.filter("get_fees")
def get_fees(ticket_price, fee):
    ticket_price = float(ticket_price)
    return ((ticket_price/100 * float(fee)) + 1)
