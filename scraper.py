from bs4 import BeautifulSoup
import requests
import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):  
  name = "quotes"  
  def __init__(self, *args, **kwargs):
    super(QuotesSpider, self).__init__(*args, **kwargs)
    query = kwargs.get('query')    
    url = 'https://www.goodreads.com/search/?q=' + query
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    results = soup.find('a', {'class': 'bookTitle'}, href=True)
    for item in results[:1]:
      self.start_urls = ['https://www.goodreads.com' + item['href']]      
      print(self.start_urls)

  def parse(self, response):
    print('lalal')
    for result in response.xpath('//*[@id="description"]//span[contains(@id, "freeText") and not(contains(@id, "Container"))]/text()'):
      items.append(result.extract())
      print(items)    



