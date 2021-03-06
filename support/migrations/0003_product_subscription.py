# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_auto_20170713_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=128)),
                ('model', models.CharField(max_length=128)),
                ('sku', models.CharField(max_length=128)),
                ('price_silver', models.FloatField(default=0.0)),
                ('price_gold', models.FloatField(default=0.0)),
                ('price_black', models.FloatField(default=0.0)),
                ('with_cloud', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('Silver', 'silver'), ('Gold', 'gold'), ('Black', 'black')], max_length=64)),
                ('price', models.FloatField(default=0.0)),
                ('discount_code', models.CharField(blank=True, max_length=64)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.Client')),
            ],
        ),
    ]
