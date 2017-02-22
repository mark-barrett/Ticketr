# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketr', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(default='static/images/ticketr.png', upload_to='images/event_images'),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketr.Category'),
        ),
    ]