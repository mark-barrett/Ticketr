from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(EventOwner)
admin.site.register(Ticket)
admin.site.register(TicketQueue)
admin.site.register(Order)
admin.site.register(ResellList)