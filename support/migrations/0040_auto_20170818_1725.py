# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-19 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0039_auto_20170817_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='release',
            field=models.DateField(blank=True, null=True),
        ),
    ]
