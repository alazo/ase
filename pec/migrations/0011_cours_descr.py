# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0010_domaine_couleur'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='descr',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
