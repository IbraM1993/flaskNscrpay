import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BbcNewsSpider(CrawlSpider):
    name = "bbc_spider"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["http://www.bbc.com/"]
    base_url = "http://www.bbc.com/"
    rules = [Rule(LinkExtractor(allow="news/"),
                    callback="parse_news_links", follow=True)]

    def parse_news_links(self, response):
        """
        Takes the response from the yielded scrapy request in self.parse (the news page link), and scrapes for the links of each article in that news page link.

        Parameters
        ----------
        response
            html response (scrapy.http.Response) object, the response is from the same class accross all functions

        Returns
        -------
        None
        """
        rsp = response.xpath("nw-o-link-split__anchor").extract_first()
        yield {"response": rsp}

    # # Spider class requirement: a function with the name "parse" must be defined
    # def parse(self, response):
    #     """
    #     Takes the html response from the home page and fetch the link for the news page.

    #     Parameters
    #     ----------
    #     response
    #         html response (scrapy.http.Response) object, the response is from the same class accross all functions

    #     Returns
    #     -------
    #     None
        
    #     """
        
    #     if response.status == 200: # if there is a response
    #         news_page_link_class = "a.module__title__link.tag--news"
    #         news_page_link = response.css(news_page_link_class).attrib["href"]

    #         # we could define a class for custom exceptions
    #         #TODO check if css class for the target a tag exists first in the html response and throw the error there if it does not
    #         if news_page_link is None:
    #             raise Exception("News page link not found: check your code or if the css selection is no longer valid...")

    #         yield scrapy.Request(news_page_link, callback=self.parse_news_links)

    # def parse_news_links(self, response):
    #     """
    #     Takes the response from the yielded scrapy request in self.parse (the news page link), and scrapes for the links of each article in that news page link.

    #     Parameters
    #     ----------
    #     response
    #         html response (scrapy.http.Response) object, the response is from the same class accross all functions

    #     Returns
    #     -------
    #     None
    #     """
    #     rsp = response.xpath("nw-o-link-split__anchor").extract_first()
    #     yield {"response": rsp}