# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0022_auto_20170609_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='careum',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='sequence',
            name='careum',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
