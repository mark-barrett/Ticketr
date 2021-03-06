# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0004_auto_20170218_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ticketr.EventOwner'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
