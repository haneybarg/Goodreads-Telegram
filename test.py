import scrapy

#--run a crawler in a script stuff
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
import requests
from bs4 import BeautifulSoup

#--run a crawler in a script stuff
items = []
class QuotesSpider(scrapy.Spider):  
  name = "quotes"  
  def __init__(self, *args, **kwargs):
    super(QuotesSpider, self).__init__(*args, **kwargs)
    query = kwargs.get('query')
    # query = '1984'
    url = 'https://www.goodreads.com/search/?q=' + query
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    self.start_urls = ['https://www.goodreads.com' + (soup.find('a', {'class': 'bookTitle'}, href=True)['href'])]
    print(self.start_urls)
  def parse(self, response):
    print('hiers')
    for result in response.xpath('//*[@id="description"]//span[contains(@id, "freeText") and not(contains(@id, "Container"))]/text()'):
      items.append(result.extract())
      print(items)

# process = CrawlerProcess()  
# process.crawl(QuotesSpider)
# process.start()

