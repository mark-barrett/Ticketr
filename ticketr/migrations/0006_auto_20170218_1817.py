# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0005_auto_20170218_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventowner',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
