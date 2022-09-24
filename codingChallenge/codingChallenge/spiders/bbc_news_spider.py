import scrapy
from scrapy.spiders import CrawlSpider

class BbcNewsSpider(scrapy.Spider):
    name = "bbc_spider"
    start_urls = ["https://www.bbc.com/"]

    def parse(self, response):
        
        news_link_class = "a.module__title__link.tag--news"
        news_link = response.css(news_link_class).attrib['href']
        news_link_text = response.css(f"{news_link_class}::text").get() # the text could be used as the name for the collection in MongoDB later on
        
        yield {"url": news_link, "url_text": news_link_text}