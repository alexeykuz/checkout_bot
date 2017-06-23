import os
import signal
import logging

from celery import task
from celery.exceptions import SoftTimeLimitExceeded

from google_express_checkout_bot import GoogleExpressCheckoutBot

logger = logging.getLogger('google_express_handler')


@task
def add_processing_of_product(order_id):
    try:
        bot = GoogleExpressCheckoutBot(order_id)
        logger.info("Process ID:" + str(bot.browser_pid))
        bot.place_an_order()
    except SoftTimeLimitExceeded as e:
        try:
            os.kill(bot.browser_pid, signal.SIGKILL)
        except Exception as e:
            logger.error("Can't kill browser process:")
            logger.error(e)
