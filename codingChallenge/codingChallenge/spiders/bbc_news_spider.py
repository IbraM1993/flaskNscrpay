import scrapy
from ..pipelines import CodingchallengePipeline
from ..items import NewsArticleItem
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)
# c_handler = logging.StreamHandler()
# logger.addHandler(c_handler)
# logger.setLevel(logging.INFO)

class BbcNewsSpider(scrapy.Spider):
    name = "bbc_spider"
    # allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com/"]
    # base_url = "http://www.bbc.com/"
    # rules = [Rule(LinkExtractor(allow="news/"),
    #                 callback="parse_news_links", follow=True)]

    # Spider class requirement: a function with the name "parse" must be defined
    bbc_pipeline = CodingchallengePipeline()

    def parse(self, response):
        """
        Takes the html response from the home page and fetch the link for the news page.

        Parameters
        ----------
        response
            html response (scrapy.http.Response) object, the response is from the same class accross all functions

        Returns
        -------
        None
        
        """
        response_status = response.status
        if response_status == 200: # if there is a response
            # could get link from navbar as well
            #TODO let the class only to be module__title__link so we can get all categories (news, sports, etc...): loop over categories in response
            news_page_link_class = "a.module__title__link.tag--news" # class of a tag for news 
            news_page_link = response.css(news_page_link_class).attrib["href"]

            # we could define a class for custom exceptions
            #TODO check if css class for the target a tag exists first in the html response and throw the error there if it does not
            if news_page_link is None:
                raise Exception("News page link not found: check your code or if the css selection is no longer valid...")

            if len(news_page_link): # len is used to avoid empty strings
                yield scrapy.Request(news_page_link, callback=self.parse_news_categories_links)
                
            else:
                logger.warning(f"Could not identify the news page link. The result was {news_page_link}...")

        else:
            logger.warning(f"The response status was {response_status}")

    def parse_news_categories_links(self, response):
        """
        Takes the response from the yielded scrapy request in self.parse (the news page link), and scrapes the links in the navbar to then scrape all
        tabs in another function (self.parse_news_articles()).

        Parameters
        ----------
        response
            html response

        Returns
        -------
        None
        """
        response_status = response.status

        if response_status == 200:
            #TODO find a way to yield the final link via a recursive process (consider digging deeper into CralwerSpider docs)
            for r in response.css("a.nw-o-link"): # class of a tags in news navigation
                
                # # some news categories contain sub-categories with links of same class => loop again
                # #TODO check if a function could be defined to process the final article link and remove redundancy
        
                news_category_link = r.css("::attr(href)").get()
                processed_news_category_link = self.bbc_pipeline.process_news_link(news_category_link)
                
                if processed_news_category_link is None:
                    continue

                final_news_category_link = urljoin(response.url, processed_news_category_link)

                yield scrapy.Request(final_news_category_link, callback=self.parse_news_sub_categories_links)

        else:
            logger.warning(f"The response status was {response_status}")
        
    def parse_news_sub_categories_links(self, response):
        """
        Takes the response from the yielded scrapy request in self.parse_news_links (for every iteration), redirects to a news article and scrapes it.

        Parameters
        ----------
        response
            html response

        Returns
        -------
        None
        """
        response_status = response.status

        if response_status == 200:

            for r in response.css("nav.nw-c-nav__wide-secondary a.nw-o-link"):
                news_sub_categories_link = r.css("::attr(href)").get()
                processed_news_sub_categories_link = self.bbc_pipeline.process_news_link(news_sub_categories_link)
                
                if processed_news_sub_categories_link is None:
                    continue

                final_news_sub_category_link = urljoin(response.url, processed_news_sub_categories_link)
                yield {"link": final_news_sub_category_link}

                yield scrapy.Request(final_news_sub_category_link, callback=self.parse_news_articles)
                
        else:
            logger.warning(f"The response status was {response_status}")

    def parse_news_articles(self, response):
        """
        Takes the response from the yielded scrapy request in self.parse_news_links (for every iteration), redirects to a news article and scrapes it.

        Parameters
        ----------
        response
            html response

        Returns
        -------
        None
        """
        response_status = response.status

        if response_status == 200:
            
            item = NewsArticleItem()
            item['title'] = response.xpath('//h1[@id="main-heading"]/text()').get()

            # yield item

        else:
            logger.warning(f"The response status was {response_status}")
