# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from scrapy.utils.project import get_project_settings

class CodingchallengePipeline:
    """
    DESCRIPTION:
    ------------
    * This pipeline is used to process data within the scraping flow.
    """
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
        """
        Takes a news article link, check for it if it is complete, and if it is not, it concatinates it to the news section link to form an acessible link.

        Parameters
        ----------
        link
            the news article link to be processed

        Returns
        -------
        processed_link
            the processed article news link that could be joined with the news URL in the spider
        """
        if "http" in link[:10]:
            return link

        else:
            return f"https://www.bbc.com{link}"

# class MongoDBPipeline(object):
#     """
#     DESCRIPTION:
#     ------------
#     * This pipeline is used to insert data in to MongoDB.
#     * MongoDB settings are provided in settings.py
#     """
#     def __init__(self):
#         """
#         Constructor for the MongoDB pipeline instance. It creates a connection and configures it based on the MongoDB settings in settings.py.
#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         object
#             an instance of the class MongoDBPipeline
#         """
#         #TODO consider security for settings (could be defined as an attribute from the spider class)
#         SETTINGS = get_project_settings()

#         self.__connection = pymongo.MongoClient(
#             host = SETTINGS["MONGODB_URI"]
#         )
#         db = self.__connection[SETTINGS["MONGODB_DB"]]
#         self.__collection = db[SETTINGS["MONGODB_COLLECTION"]]

#     def process_item(self, item: dict, spider):
#         """
#         Inserts an item into the MongoDB collection.

#         Parameters
#         ----------
#         item
#             the dictionary that contains the yielded item from scraping a news article.

#         spider
#             the scrapy crawler

#         Returns
#         -------
#         object
#             an instance of the class MongoDBPipeline 
#         """
#         self.__collection.insert_one(dict(item))

    # def close_connection(self, spider):
    #     """
    #     Closes the connection with MongoDB.

    #     Parameters
    #     ----------
    #     spider
    #         the scrapy crawler

    #     Returns
    #     -------
    #     None    
    #     """
    #     self.__connection.close()