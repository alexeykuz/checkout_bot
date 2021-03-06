# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_app', '0008_auto_20170619_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='id_in_file',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Id of order in file'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Product order is created'), (2, 'Handling order'), (3, 'Order is processed'), (4, 'Order is processed with errors'), (5, 'Product is sold out'), (6, 'Product order is stopped')], default=1, verbose_name='Status of order'),
        ),
    ]
