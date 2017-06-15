# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_app', '0002_auto_20170607_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='buyer_address2',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Buyer address 2'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Product order created'), (2, 'Handling order'), (3, 'Order processed'), (4, 'Order processed with errors'), (5, 'Product sold out')], default=1, verbose_name='Status of order'),
        ),
    ]
