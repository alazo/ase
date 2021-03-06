# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0018_auto_20170608_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sequence',
            old_name='objectifs',
            new_name='objectifs_evaluateurs',
        ),
        migrations.AddField(
            model_name='cours',
            name='didactique',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='cours',
            name='evaluation',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='sequence',
            name='careum',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='sequence',
            name='objectifs_apprentissage',
            field=models.TextField(blank=True),
        ),
    ]
