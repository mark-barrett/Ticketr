# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0042_order_for_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='for_sale',
            field=models.BooleanField(default=False),
        ),
    ]
