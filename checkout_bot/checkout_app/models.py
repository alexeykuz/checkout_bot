# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

STATE_CREATED = 1
STATE_IN_PROCESS = 2
STATE_SUCCESS_FINISHED = 3
STATE_ERROR = 4
STATE_SOLD_OUT = 5

STATE_CHOICES = (
    (STATE_CREATED, _('Product order created')),
    (STATE_IN_PROCESS, _('Handling order')),
    (STATE_SUCCESS_FINISHED, _('Order processed')),
    (STATE_ERROR, _('Order processed with errors')),
    (STATE_SOLD_OUT, _('Product sold out')),
)


class OrdersFileList(models.Model):
    file_name = models.CharField(
        default=None, null=True, blank=True,
        max_length=120, verbose_name=_('Name of file with orders'))

    def __str__(self):
        return self.file_name


class ProductOrder(models.Model):
    product_url = models.CharField(
        default=None, null=True, blank=True,
        max_length=255, verbose_name=_('Product url'))
    product_name = models.CharField(
        default=None, null=True, blank=True,
        max_length=255, verbose_name=_('Product name'))
    product_buyer = models.CharField(
        default=None, null=True, blank=True,
        max_length=120, verbose_name=_('Product buyer'))
    buyer_address = models.CharField(
        default=None, null=True, blank=True,
        max_length=255, verbose_name=_('Buyer address'))
    buyer_address2 = models.CharField(
        default=None, null=True, blank=True,
        max_length=255, verbose_name=_('Buyer address 2'))
    buyer_city = models.CharField(
        default=None, null=True, blank=True,
        max_length=120, verbose_name=_('Buyer city'))
    buyer_state_code = models.CharField(
        default=None, null=True, blank=True,
        max_length=25, verbose_name=_('Buyer state code'))
    buyer_postal_code = models.CharField(
        default=None, null=True, blank=True,
        max_length=25, verbose_name=_('Buyer postal code'))
    status = models.SmallIntegerField(
        default=1, choices=STATE_CHOICES, verbose_name=_('Status of order'))
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date created'))
    date_started = models.DateTimeField(
        blank=True, null=True, verbose_name=_('Date started'))
    orders_file = models.ForeignKey(
        'OrdersFileList', null=True, blank=True,
        verbose_name=_('Orders file list instance'))

    def as_dict(self):
        return {
            'id': self.id,
            'product_url': self.product_url,
            'product_name': self.product_name,
            'status': self.status,
            'date_created': self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'date_started': self.date_started.strftime("%Y-%m-%d %H:%M:%S"),
            'status_text': self.get_status_display(),
        }

    def __str__(self):
        return self.product_url if self.product_url else str(self.id)
