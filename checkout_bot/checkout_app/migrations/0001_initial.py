# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersFileList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Name of file with orders')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_url', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Product url')),
                ('product_name', models.IntegerField(blank=True, default=None, null=True, verbose_name='Product name')),
                ('status', models.SmallIntegerField(choices=[(1, 'Search in process'), (2, 'Search is finished'), (3, 'Search has errors')], default=1, verbose_name='Status of order')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_started', models.DateTimeField(auto_now_add=True, verbose_name='Date started')),
            ],
        ),
    ]