# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0058_eventowner_paypal_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='reselllist',
            name='paypal_email',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]