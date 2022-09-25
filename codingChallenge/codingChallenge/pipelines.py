# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CodingchallengePipeline:
    def process_item(self, item, spider):
        return item

    def process_news_link(self, news_link: str) -> str:
        # "/news" is the home button for the news page itself (we do not want it)
        # if "/news" is not in the link, then it is not something related to news
        if news_link == "/news" or "/news" not in news_link or news_link is None:
            return None

        if len(news_link): # if it is a link
            #TODO remove this block and handle live news link (present in each)
            news_article_category = news_link.split("/")[2]
            if news_article_category == "live":
                return None
            
            preprocessed_news_link = "/".join(news_link.split("/")[1:]) # removing the empty string and the word news as news already present in response.url
            
            return preprocessed_news_link
