from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms import validators, SubmitField

import helpers as helpers

from codingChallenge.codingChallenge.spiders import bbc_news_spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)

app.config["SECRET_KEY"] = "abc123!@#"

MONGO_URI = "mongodb+srv://IbraM:1993@cluster0.8hgixtg.mongodb.net/bbc"
app.config["MONGO_URI"] = MONGO_URI
connection = PyMongo(app)

process = CrawlerProcess(get_project_settings())

class RunScraping(FlaskForm):
    run_scraping_input = StringField("run_scraping", validators=(validators.DataRequired(),))
    submit = SubmitField("Submit")

class SearchKeyword(FlaskForm):
    search_keyword_input = StringField("search_keyword", validators=(validators.DataRequired(),))
    submit = SubmitField("Submit")

# keyword = helpers.get_keyword_from_CLI()

@app.route("/", methods=["GET", "POST"])
def home():
    """ Renders the home page which consists of two links: "News to all the news, and News by Keyword for the filtered news based on user input """
    run_scraping = RunScraping()
    data = {"run_scraping": run_scraping}

    if run_scraping.validate_on_submit():
        run_scraping_val = run_scraping.run_scraping_input.data
        
        if helpers.check_if_no_articles_in_db(connection, run_scraping_val):
            process.crawl(bbc_news_spider.BbcNewsSpider)
            process.start()
    
    return render_template("home.html", data=data)

@app.route("/news", methods=["GET", "POST"])
def news():
    """ Renders the news page which consists of all the news articles in the database """
    search_keyword = SearchKeyword()
    search_keyword_val = ""
    if search_keyword.validate_on_submit():
        search_keyword_val = search_keyword.search_keyword_input.data
    data = {"search_keyword": search_keyword_val}
    
    
    
    data["json_data"] = helpers.get_all_news_articles(connection)
    
    return render_template("news.html", data=data)

@app.route("/news_by_keyword", methods=["GET", "POST"])
def news_by_keyword():
    """ Renders the news by keyword page which consists of filtered news based on user input """
    # keyword = input("Input keyword to query DB:\n")

    data = request.form
    search_keyword_val = data["search_keyword"]

    return render_template("news_by_keyword.html", data=helpers.get_news_articles_by_keyword(connection, search_keyword_val))

if __name__ == '__main__':
    app.run(debug=True)