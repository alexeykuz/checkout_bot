import logging

from celery import task

from google_express_checkout_bot import GoogleExpressCheckoutBot

logger = logging.getLogger('google_express_handler')


@task
def add_processing_of_product(order_id):
    bot = GoogleExpressCheckoutBot(order_id)
    bot.place_an_order()
