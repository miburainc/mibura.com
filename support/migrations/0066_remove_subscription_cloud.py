# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-27 23:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0065_auto_20170927_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='cloud',
        ),
    ]
