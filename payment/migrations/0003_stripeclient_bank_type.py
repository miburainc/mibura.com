# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20170928_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripeclient',
            name='bank_type',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]