# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0007_auto_20170601_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='cours',
            name='domaine',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pec.Domaine'),
        ),
    ]
