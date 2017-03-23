# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 16:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0021_auto_20170310_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketr.Ticket')),
            ],
        ),
    ]