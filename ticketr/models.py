from __future__ import unicode_literals

from django.db import models

from datetime import *

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

    def __str__(self):
        return self.name


class Event(models.Model):
    # Varchar with 32 chars
    name = models.CharField(max_length=32)
    # Give the event a picture
    image = models.CharField(max_length=128)

    # Start date and time and end date and time
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    end_time = models.TimeField(auto_now_add=True)

    description = models.TextField()

    # Every product has a category
    category = models.ForeignKey(Category)

    event_owner = models.ForeignKey(EventOwner, default=1)

    ticket_price = models.FloatField(max_length=20, default=0)

    # String function to display event
    def __str__(self):
        return self.name