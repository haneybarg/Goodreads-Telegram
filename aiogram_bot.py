import asyncio
import logging
from aiogram import Bot, types, Dispatcher, executor
from test import items, QuotesSpider
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

API_TOKEN = '710421060:AAH7IffP-JE5Dt4-Eu4EFy0TzXOY9iUl9Kg'

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)


@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
  query = inline_query.query  
  process = CrawlerProcess()
  process.crawl(QuotesSpider, query=query)
  process.start()  
  input_content = types.InputTextMessageContent("". join(items))
  item = types.InlineQueryResultArticle(id='1', title='echo',
                                        input_message_content=input_content)
  await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


if __name__ == '__main__':
  executor.start_polling(dp, loop=loop, skip_updates=True)

