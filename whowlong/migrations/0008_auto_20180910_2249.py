# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-10 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whowlong', '0007_auto_20180910_2232'),
    ]

    operations = [
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
