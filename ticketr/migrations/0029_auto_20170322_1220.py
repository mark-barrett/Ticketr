# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 12:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0028_auto_20170322_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='active',
            new_name='used',
        ),
    ]