# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0007_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('servers', 'Servers'), ('storage', 'Storage Appliances'), ('firewall', 'Firewalls'), ('netswitch', 'Network Switches')], max_length=32),
        ),
    ]
