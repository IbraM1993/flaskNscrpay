from flask import Flask, render_template
from flask_pymongo import PyMongo

import helpers as helpers

from codingChallenge.codingChallenge.spiders import bbc_news_spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)

MONGO_URI = "mongodb+srv://IbraM:1993@cluster0.8hgixtg.mongodb.net/bbc"
app.config["MONGO_URI"] = MONGO_URI

connection = PyMongo(app)
# keyword = helpers.get_keyword_from_CLI()

if helpers.check_if_no_articles_in_db(connection):
    process = CrawlerProcess(get_project_settings())
    process.crawl(bbc_news_spider.BbcNewsSpider)
    process.start()

@app.route("/")
def home():
    """ Renders the home page which consists of two links: "News to all the news, and News by Keyword for the filtered news based on user input """
    return render_template("home.html")

@app.route("/news", methods=["GET"])
def news():
    """ Renders the news page which consists of all the news articles in the database """
    return render_template("news.html", data=helpers.get_all_news_articles(connection))

@app.route("/news_by_keyword", methods=["GET"])
def news_by_keyword():
    """ Renders the news by keyword page which consists of filtered news based on user input """
    keyword = input("Input keyword to query DB:\n")
    return render_template("news_by_keyword.html", data=helpers.get_news_articles_by_keyword(connection, keyword))

if __name__ == '__main__':
    app.run()