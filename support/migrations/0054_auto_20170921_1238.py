# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 19:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0053_purchaseorder_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudAddOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('cloud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.Cloud')),
            ],
        ),
        migrations.AddField(
            model_name='clientproduct',
            name='cloud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='support.Cloud'),
        ),
    ]