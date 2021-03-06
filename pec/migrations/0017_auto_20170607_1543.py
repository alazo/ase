# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pec', '0016_auto_20170606_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(unique=True)),
                ('nom', models.CharField(blank=True, max_length=50)),
                ('periode', models.IntegerField()),
                ('contenu', models.TextField(blank=True)),
                ('objectifs', models.ManyToManyField(blank=True, to='pec.ObjectifEvaluateur')),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pec.Cours')),
            ],
        ),
        migrations.AddField(
            model_name='lecon',
            name='sequence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pec.Sequence'),
        ),
    ]
