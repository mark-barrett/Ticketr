# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 21:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0054_invitecode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_time',
        ),
    ]
