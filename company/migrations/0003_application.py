# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20170727_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('position', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=64)),
                ('cover', models.TextField()),
                ('comments', models.CharField(blank=True, max_length=500)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Job')),
            ],
        ),
    ]
