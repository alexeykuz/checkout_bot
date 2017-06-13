# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand, CommandError

from checkout_app.google_express_checkout_bot import \
    GoogleExpressCheckoutBot


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            bot = GoogleExpressCheckoutBot()
            bot.place_an_order()
        except Exception:
            raise CommandError('Bot not running')
