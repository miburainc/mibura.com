# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 20:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0060_unknownproduct_release'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cloud',
        ),
        migrations.RemoveField(
            model_name='unknownproduct',
            name='release',
        ),
    ]