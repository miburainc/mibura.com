# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 19:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='position',
        ),
    ]
