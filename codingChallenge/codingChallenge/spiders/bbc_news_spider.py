import scrapy

class BbcNewsSpider(scrapy.Spider):
    name = "bbc_spider"
    start_urls = ["https://www.bbc.com/"]

    def parse(self, response):
        
        news_page_link_class = "a.module__title__link.tag--news"
        news_page_link = response.css(news_page_link_class).attrib['href']
        news_page_link_text = response.css(f"{news_page_link_class}::text").get() # the text could be used as the name of the collection in MongoDB later on

        yield {"url": news_page_link, "url_text": news_page_link_text}

        if news_page_link:
            yield scrapy.Request(news_page_link, callback=self.parse_news)

    def parse_news(self, response):
        rsp = response.css("a.gs-c-promo-heading.gs-o-faux-block-link__overlay-link.gel-pica-bold.nw-o-link-split__anchor").extract_first()
        yield {"response": rsp}