from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from flask_executor import Executor
from wtforms.fields import StringField
from wtforms import validators, SubmitField

from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from codingChallenge.codingChallenge.spiders.bbc_news_spider import BbcNewsSpider

import helpers as helpers
import time
import os

import crochet
crochet.setup()

app = Flask(__name__)

app.config["SECRET_KEY"] = "abc123!@#"

MONGO_URI = "mongodb+srv://IbraM:1993@cluster0.8hgixtg.mongodb.net/bbc"
app.config["MONGO_URI"] = MONGO_URI
connection = PyMongo(app)

# settings_file_path = "codingChallenge.codingChallenge.settings"
# os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
SPIDER_SETTINGS = get_project_settings()
runner = CrawlerRunner(SPIDER_SETTINGS)

class RunScraping(FlaskForm):
    run_scraping_input = StringField("run_scraping", validators=(validators.DataRequired(),))
    submit = SubmitField("Submit")

class SearchKeyword(FlaskForm):
    search_keyword_input = StringField("search_keyword", validators=(validators.DataRequired(),))
    submit = SubmitField("Submit")

# keyword = helpers.get_keyword_from_CLI()

@app.route("/")
def home():
    """ Renders the home page which consists of two links: "News to all the news, and News by Keyword for the filtered news based on user input """
    run_scraping = RunScraping()
    data = {"run_scraping": run_scraping}
    
    return render_template("home.html", data=data)

@app.route("/", methods=["POST"])
def submit():
    if request.method == "POST":
        request_data = request.form
        run_scraping_val = request_data["run_scraping"]
        if helpers.check_if_no_articles_in_db(connection, run_scraping_val):
            return redirect(url_for("scrape")) # Passing to the Scrape function

        else:
            return redirect(url_for("news"))

@app.route("/scrape")
def scrape():
    scrape_with_crochet()
    time.sleep(50)
    return redirect(url_for("news"))

@crochet.run_in_reactor
def scrape_with_crochet():
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

     # This will connect to the BbcNewsSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = runner.crawl(BbcNewsSpider)
    return eventual

def _crawler_result(item, response, spider):
    helpers.inster_to_db(connection, dict(item))

@app.route("/news", methods=["GET", "POST"])
def news():
    """ Renders the news page which consists of all the news articles in the database """
    search_keyword = SearchKeyword()
    search_keyword_val = search_keyword.search_keyword_input.data
    data = {"search_keyword": search_keyword_val}
    
    data["json_data"] = helpers.get_all_news_articles(connection)
    print(1)
    
    return render_template("news.html", data=data)

@app.route("/news_by_keyword", methods=["GET", "POST"])
def news_by_keyword():
    """ Renders the news by keyword page which consists of filtered news based on user input """
    # keyword = input("Input keyword to query DB:\n")

    request_data = request.form
    search_keyword_val = request_data["search_keyword"]

    return render_template("news_by_keyword.html", data=helpers.get_news_articles_by_keyword(connection, search_keyword_val))

if __name__ == '__main__':
    # to scrape in the background
    # app.config["EXECUTOR_TYPE"] = "thread"
    # app.config["CUSTOM_EXECUTOR_MAX_WORKERS"] = 5
    # executor = Executor(app, name="custom")

    app.run()