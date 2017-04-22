from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from datetime import *

from django.conf import settings

# Create database tables by creating classes that extend the model class
from django.forms import ImageField


class Category(models.Model):
    name = models.CharField(max_length=16)

    # String function to display event
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class EventOwner(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    website = models.CharField(max_length=64)
    facebook = models.CharField(max_length=64)
    owner = models.ForeignKey(User)
    image = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Event(models.Model):
    # Varchar with 32 chars
    name = models.CharField(max_length=64)
    # Give the event a picture
    image = models.CharField(max_length=240)
    background = models.CharField(max_length=240)

    # Start date and time and end date and time
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()

    description = models.TextField()

    # Every product has a category
    category = models.ForeignKey(Category)

    event_owner = models.ForeignKey(EventOwner, default=1)

    location = models.CharField(max_length=60)

    privacy = models.CharField(max_length=80)

    resell = models.CharField(max_length=80)

    resell_when = models.CharField(max_length=80)

    resell_amount = models.IntegerField()

    # String function to display event
    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)

    # Link ticket to an event
    event = models.ForeignKey(Event)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'tickets'


class TicketQueue(models.Model):
    ticket = models.ForeignKey(Ticket)
    token = models.CharField(max_length=64)
    ticket_quantity = models.IntegerField()
    time_inserted = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.token


class Order(models.Model):
    order_number = models.CharField(max_length=16)
    ticket = models.ForeignKey(Ticket)
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    order_code = models.CharField(max_length=24)
    used = models.BooleanField()
    for_sale = models.BooleanField(default=False)
    qrcode = models.FileField(upload_to='qrcode', blank=True, null=True)
    payment_amount = models.DecimalField(decimal_places=2, max_digits=6)
    order_date = models.DateField()
    order_time = models.TimeField()

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name_plural = 'orders'


class ResellList(models.Model):
    order = models.ForeignKey(Order)
    event = models.ForeignKey(Event)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    reason = models.TextField()

    def __str__(self):
        return self.order.order_number

    class Meta:
        verbose_name_plural = 'ResellLists'


class DiscountCode(models.Model):
    code = models.CharField(max_length=64)
    discount = models.DecimalField(decimal_places=2, max_digits=6)
    event = models.ForeignKey(Event)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Discount Codes'


class Request(models.Model):
    did_you = models.BooleanField()
