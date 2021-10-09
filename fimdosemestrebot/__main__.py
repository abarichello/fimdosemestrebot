import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    InlineQueryHandler,
    Filters,
    MessageHandler,
)

import fimdosemestrebot.core as core
import fimdosemestrebot.config as config

logging.basicConfig(
    format='%(asctime)s -%(name)s-%(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def error_callback(bot, update, error):
    logging.error(error)


updater = Updater(
    token=config.FDS_TOKEN, request_kwargs={'read_timeout': 10, 'connect_timeout': 7}
)
dp = updater.dispatcher
job = updater.job_queue

dp.add_error_handler(error_callback)
dp.add_handler(CommandHandler('start', core.start))
dp.add_handler(
    CommandHandler('set', core.set_date, pass_job_queue=True, pass_chat_data=True)
)
dp.add_handler(CommandHandler('help', core.get_help))
dp.add_handler(InlineQueryHandler(core.inline))

updater.start_polling()
updater.idle()
