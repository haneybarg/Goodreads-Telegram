import asyncio
import html.parser
import logging
import requests
from aiogram import Bot, types, Dispatcher, executor
from bs4 import BeautifulSoup


BOT_TOKEN = 'INSERT TELEGRAM TOKEN'
GR_TOKEN = 'INSERT GOODREADS TOKEN'

logging.basicConfig(level = logging.DEBUG)

loop = asyncio.get_event_loop()
bot = Bot(token = BOT_TOKEN, loop = loop)
dp = Dispatcher(bot)


class HTMLTextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super(HTMLTextExtractor, self).__init__()
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def get_text(self):
        return ''.join(self.result)


@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
  query = inline_query.query

  page = requests.get(
    "https://www.goodreads.com/book/title.xml?key=" + GR_TOKEN + "&title=" + query
  )

  soup = BeautifulSoup(page.content, 'xml')

  html_extractor = HTMLTextExtractor()
  html_extractor.feed(soup.find('description').text)
  text = html_extractor.get_text()

  rating = soup.find('average_rating').text
  photo_url = soup.find('image_url').text
  thumb_url = soup.find('small_image_url').text

  await bot.answer_inline_query(
    inline_query.id,
    results = [
      types.InlineQueryResultArticle(
        id = '1',
        title = query,
        input_message_content = types.InputTextMessageContent(
          "\n".join([
            "Rating: " + rating,
            "",
            text,
            "[​​​​​​​​​​​](" + photo_url + ")"
          ]),
          parse_mode = 'markdown',
        ),
        thumb_url = thumb_url,
        thumb_width = 200,
        thumb_height = 200
      )
    ],
    cache_time = 1
  )


if __name__ == '__main__':
  executor.start_polling(dp, loop = loop, skip_updates = True)

