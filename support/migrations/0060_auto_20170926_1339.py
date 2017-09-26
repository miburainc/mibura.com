# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0059_auto_20170925_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientproduct',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clientproduct',
            name='unknown',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='support.UnknownProduct'),
        ),
    ]
