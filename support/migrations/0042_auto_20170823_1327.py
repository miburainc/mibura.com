# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-23 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0041_auto_20170823_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subtotal',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='cloud',
            field=models.ManyToManyField(blank=True, to='support.Cloud'),
        ),
    ]
