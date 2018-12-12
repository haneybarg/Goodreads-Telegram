
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

from telegram.utils.helpers import escape_markdown

from telegram import InlineQueryResultArticle, ParseMode, \
  InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging
from twisted.internet import reactor
from test import QuotesSpider, items

from scrapy                 import signals
from scrapy.crawler         import CrawlerRunner
from pydispatch             import dispatcher
from scrapy.utils.project   import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging


from bs4 import BeautifulSoup
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
  """Send a message when the command /start is issued."""
  update.message.reply_text('Hi!')

def inlinequery(bot, update, signal=signals.item_passed):
  """Handle the inline query."""
  query = update.inline_query.query
  print(query)
  if(query[-1] == '.'):
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()
    d = runner.crawl(QuotesSpider(query=query))
    d.addBoth(lambda _: reactor.stop())
    reactor.run(0)
    print('hiers')
    results = [InlineQueryResultArticle(
      id="1",
      title=query,
      input_message_content=InputTextMessageContent(items))]
    
    update.inline_query.answer(results)
    
def error(bot, update, error):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, error)


def main():
  # Create the Updater and pass it your bot's token.
    updater = Updater("710421060:AAH7IffP-JE5Dt4-Eu4EFy0TzXOY9iUl9Kg")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # on noncommand i.e message - echo the message on Telegram    
    dp.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling(poll_interval = 1.0,timeout=20)    
    # log all errors
    dp.add_error_handler(error)

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
  main()        

