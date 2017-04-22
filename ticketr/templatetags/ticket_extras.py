from django import template
from datetime import date

register = template.Library()


@register.filter("remove_key")
def remove_key(value, arg):
    return value.split(arg)[0]


@register.filter("get_fees_total")
def get_fees_total(ticket_price, fee):
    ticket_price = float(ticket_price)

    # Accomadate free tickets
    if ticket_price > 0:
        return ((ticket_price/100 * float(fee)) + 1) + ticket_price
    else:
        return 0


@register.filter("get_fees")
def get_fees(ticket_price, fee):
    ticket_price = float(ticket_price)

    # Accomadate free tickets
    if ticket_price > 0:
        return (ticket_price/100 * float(fee)) + 1
    else:
        return 0


@register.filter("is_past_due")
def is_past_due(self):
    return date.today() > self.date
