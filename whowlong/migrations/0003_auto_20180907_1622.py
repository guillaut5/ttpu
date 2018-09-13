# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-07 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whowlong', '0002_auto_20180907_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='label',
        ),
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.FloatField(blank=True, default=float("nan"), null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='lon',
            field=models.FloatField(blank=True, default=float("nan"), null=True),
        ),
    ]