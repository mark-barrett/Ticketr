# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0040_reselllist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reselllist',
            name='user',
        ),
    ]