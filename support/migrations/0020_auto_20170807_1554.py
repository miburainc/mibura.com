# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0019_auto_20170807_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('none', '**No Category**'), ('servers', 'Servers'), ('storage', 'Storage Appliances'), ('network', 'Networking'), ('appliances', 'Appliances')], max_length=32),
        ),
    ]