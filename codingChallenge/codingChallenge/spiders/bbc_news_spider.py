import scrapy

class BbcNewsSpider(scrapy.Spider):
    name = "bbc_spider"
    start_urls = ["https://www.bbc.com/"]

    # Spider class requirement: a function with the name "parse" must be defined
    def parse(self, response):
        
        if response.status == 200: # if there is a response
            news_page_link_class = "a.module__title__link.tag--news"
            news_page_link = response.css(news_page_link_class).attrib['href']

            # we could define a class for custom exceptions
            #TODO check if css class for the target a tag exists first in the html response and throw the error there if it does not
            if news_page_link is None:
                raise Exception("News page link not found: check your code or if the css selection is no longer valid...")

            yield scrapy.Request(news_page_link, callback=self.parse_news)

    def parse_news(self, response):
        rsp = response.css("a.gs-c-promo-heading.gs-o-faux-block-link__overlay-link.gel-pica-bold.nw-o-link-split__anchor").extract_first()
        yield {"response": rsp}