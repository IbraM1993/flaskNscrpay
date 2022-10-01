# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    authors = scrapy.Field()
    article_date = scrapy.Field()
    tags_text = scrapy.Field()
    tags_links = scrapy.Field()
    article_text = scrapy.Field()
    url = scrapy.Field()
    related_stories = scrapy.Field()
    related_topics = scrapy.Field()
    CREATED = scrapy.Field()
