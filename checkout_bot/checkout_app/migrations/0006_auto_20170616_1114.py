# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 11:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_app', '0005_auto_20170616_0800'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorder',
            old_name='products_bought',
            new_name='products_available',
        ),
    ]
