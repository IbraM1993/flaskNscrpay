# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CodingchallengePipeline:
    def process_item(self, item, spider):
        return item

    def process_news_categories_link(self, link: str) -> str:
        """
        Takes a news link and processes it in a way that, once returned, it could be joined with the news URL in the spider (bbc_news_spider.py) to form an accessible link.

        Parameters
        ----------
        link
            the news link to be processed

        Returns
        -------
        processed_link
            the processed news link that could be joined with the news URL in the spider

        """
        # "/news" is the home button for the news page itself (we do not want it)
        # if "/news" is not in the link, then it is not something related to news
        if link == "/news" or "/news" not in link or link is None:
            return None

        if len(link): # if it is a link
            #TODO remove this block and handle live news link (present in each)
            news_article_category = link.split("/")[2]
            if news_article_category == "live":
                return None
            
            processed_link = "/".join(link.split("/")[1:]) # removing the empty string and the word news as news already present in response.url
            
            return processed_link

    def process_news_sub_categories_links(self, link: str) -> str:
        """
        Takes a news link and processes it in a way that, once returned, it could be joined with the news URL in the spider (bbc_news_spider.py) to form an accessible link.

        Parameters
        ----------
        news_link
            the news link to be processed

        Returns
        -------
        processed_link
            the processed news link that could be joined with the news URL in the spider

        """        
        processed_link = link.split("news/")[1]
        if "/" != processed_link[0]:
            processed_link = f"/{processed_link}/"
        
        return processed_link

    def process_news_articles_links(self, link: str) -> str:
        if "http" in link[:10]:
            return link

        else:
            return f"https://www.bbc.com{link}"