# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0029_auto_20170322_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.TextField(),
        ),
    ]
