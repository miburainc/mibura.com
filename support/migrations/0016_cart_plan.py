# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0015_auto_20170803_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='plan',
            field=models.CharField(choices=[('slvr', 'Silver'), ('gold', 'Gold'), ('blck', 'Black')], default='', max_length=32),
            preserve_default=False,
        ),
    ]