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

    resell_amount = models.CharField(max_length=80)

    # String function to display event
    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField()

    # Link ticket to an event
    event = models.ForeignKey(Event)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'tickets'


