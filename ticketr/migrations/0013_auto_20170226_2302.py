# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0012_eventowner_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventowner',
            name='description',
        ),
        migrations.AddField(
            model_name='eventowner',
            name='facebook',
            field=models.CharField(default=django.utils.timezone.now, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventowner',
            name='website',
            field=models.CharField(default=django.utils.timezone.now, max_length=64),
            preserve_default=False,
        ),
    ]