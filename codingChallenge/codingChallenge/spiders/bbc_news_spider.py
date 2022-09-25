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
        Takes the response from the yielded scrapy request in self.parse() (the news page link), and scrapes the links in the navbar to get the news categories links.
        It then yields a request to self.parse_news_sub_categories_links() to scrape the news sub-categories links.

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
            #TODO find a way to yield the final link via a recursive process (consider digging deeper into CralwerSpider docs: seems easy automation once docs are understood)
            for r in response.css("nav.nw-c-nav__wide a.nw-o-link"): # class of a tags in news navigation
                
                # # some news categories contain sub-categories with links of same class => loop again
                # #TODO check if a function could be defined to process the final article link and remove redundancy
        
                news_category_link = r.css("::attr(href)").get()
                processed_news_category_link = self.bbc_pipeline.process_news_categories_link(news_category_link)
                
                if processed_news_category_link is not None:
                    final_news_category_link = urljoin(response.url, processed_news_category_link)
                    yield scrapy.Request(final_news_category_link, callback=self.parse_news_sub_categories_links)

        else:
            logger.warning(f"The response status was {response_status}")
        
    def parse_news_sub_categories_links(self, response):
        """
        Takes the response from the yielded scrapy request in self.parse_news_categories_links() (for every iteration), to then scrape all the news sub-categories in each
        category (e.g., Africa and Europe in World). It then yields a request to self.parse_news_articles_links() to scrape the news articles links within a sub-category.

        Parameters
        ----------
        response
            html response

        Returns-
        -------
        None
        """
        response_status = response.status
        if response_status == 200:
            sub_links_response = response.css("nav.nw-c-nav__wide-secondary a.nw-o-link")
            res = sub_links_response.get()

            if res is None:
                for r in response.css("a.gs-c-promo-heading.gs-o-faux-block-link__overlay-link.nw-o-link-split__anchor"):
                    news_articles_link = r.css("::attr(href)").get()
                    processed_news_category_link = self.bbc_pipeline.process_news_articles_links(news_articles_link)
                    yield scrapy.Request(processed_news_category_link, callback=self.parse_news_article_items)

            else:
                for r in sub_links_response:
                    news_sub_categories_link = r.css("::attr(href)").get()
                    
                    if news_sub_categories_link is not None:
                        if "http" in news_sub_categories_link:
                            final_news_sub_category_link = news_sub_categories_link
                        else:
                            final_news_sub_category_link = urljoin(response.url, news_sub_categories_link)
                    
                    yield scrapy.Request(final_news_sub_category_link, callback=self.parse_news_sub_categories_links)
                    
        else:
            logger.warning(f"The response status was {response_status}")
    
    def parse_news_article_items(self, response):
        """
        Takes the response (the link for a news article) from the yielded scrapy request in self.parse_news_articles_links() (for every iteration),
        and scrapes the available info in a news article. It then yields a JSON object containing the scraped info.

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
            title = response.xpath('//h1[@id="main-heading"]/text()').get()
            if title is not None:
                item['title'] = title
                item['category'] = ""

                authors = response.xpath('//*[@id="main-content"]/div[5]/div/div[1]/article/header/p/span/strong//text()').get()
                if authors is not None:
                    if "by " == authors[:3].lower():
                        authors = authors[3:]
                else:
                    authors = ""
                item["authors"] = authors

                

                yield item

        else:
            logger.warning(f"The response status was {response_status}")
