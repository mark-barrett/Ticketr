from __future__ import unicode_literals

from django.db import models


# Create database tables by creating classes that extend the model class
class Category(models.Model):
    name = models.CharField(max_length=16)

    # String function to display event
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Event(models.Model):
    # Varchar with 32 chars
    name = models.CharField(max_length=32)
    description = models.TextField()
    # Every product has a category
    category = models.ForeignKey(Category)

    # String function to display event
    def __str__(self):
        return self.name