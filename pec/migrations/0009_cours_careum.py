# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0008_cours_domaine'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='careum',
            field=models.CharField(default='', max_length=10),
        ),
    ]