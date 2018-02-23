# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0006_auto_20170601_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='type',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='cours',
            name='objectifs_evaluateurs',
            field=models.ManyToManyField(blank=True, to='pec.ObjectifEvaluateur'),
        ),
    ]
