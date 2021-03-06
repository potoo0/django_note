# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-05-02 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_name', models.CharField(max_length=50)),
                ('g_customer', models.ManyToManyField(to='app_manyToMany.Customer')),
            ],
            options={
                'verbose_name': 'Goods',
                'verbose_name_plural': 'Goodss',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
