# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-29 23:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_merge_20170929_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='subscription',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
    ]