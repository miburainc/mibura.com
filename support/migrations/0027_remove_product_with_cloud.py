# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 03:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0026_auto_20170809_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='with_cloud',
        ),
    ]
