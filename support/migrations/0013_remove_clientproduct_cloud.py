# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0012_auto_20170803_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientproduct',
            name='cloud',
        ),
    ]