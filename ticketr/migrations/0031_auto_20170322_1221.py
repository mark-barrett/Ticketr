# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0030_auto_20170322_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=16),
        ),
    ]
