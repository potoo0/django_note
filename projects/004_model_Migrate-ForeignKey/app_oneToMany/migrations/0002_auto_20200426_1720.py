# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-04-26 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_oneToMany', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='s_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_oneToMany.Grade'),
        ),
    ]