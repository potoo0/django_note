# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-04-19 11:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IDcard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_num', models.CharField(max_length=18, unique=True)),
            ],
            options={
                'verbose_name': 'IDcard',
                'verbose_name_plural': 'IDcards',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=16)),
                ('p_sex', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='idcard',
            name='id_person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_oneToOne.Person'),
        ),
    ]
