from flask_pymongo import PyMongo

import json
from bson import json_util

import sys

def get_keyword_from_CLI() -> str:
    """
    Takes no arguments and get the keyword from the list of input arguments to the CLI.

    Parameters
    ----------
    None

    Returns
    -------
    keyword
        the input search keyword from the user
    """
    args_list = sys.argv
    i, nargs = 0, len(args_list)
    keyword = ""
    while i < nargs:
        if args_list[i] == "--keyword":
            i += 1

            if i < len(args_list):
                keyword = args_list[i]
        
        i += 1

    return keyword

def to_json(data) -> str:
    """
    Convert input data to JSON format.
    
    Parameters
    ----------
    data
        the input data to be processed

    Returns
    -------
    str
        a JSON format of the input data
    """
    return json.dumps(data, default=json_util.default)

def check_if_no_articles_in_db(connection: PyMongo, run_scraping: str) -> bool:
    #TODO remove function once a scheduler for the spcaring is implemented
    """
    Queries the database for a single entry to find out if any data exist. If so, this will prevent the scraping from running.
    Also, the user might specify to run the scrape when the application runs for the first time.
    
    Parameters
    ----------
    connection
        the MongoDB connection

    run_scraping
        user choice regarding whether to run scraping or not even if there were data in the database

    Returns
    -------
    bool
        True if an item was found; False otherwise
    """
    result = connection.db.news.find_one()
    # if there is an item in the DB
    if result:
        # run_scraping = input("Would you like to run the scarping? yes for yes and no for no...\n") # ask user if he wants to re-run the scrapes
        # run_scraping = "No"
        if run_scraping.lower()[0] == "y":
            return True

        return False # user does not want to re-run the scraping
    
    return True # no items in DB => don't ask user and run scraping (we could inform him of that...)

def get_all_news_articles(connection: PyMongo) -> str:
    """
    Queries the database for all news.
    
    Parameters
    ----------
    connection
        the MongoDB connection

    Returns
    -------
    str
        a JSON format of the data fetched from the queried MongoDB object
    """
    results = connection.db.news.find()
    
    news_articles = [ result for result in results ]
    return to_json(news_articles)

def get_news_articles_by_keyword(connection: PyMongo, keyword: str) -> str:
    """
    Queries the database for all news where the keyword is available in the article title or text.
    
    Parameters
    ----------
    connection
        the MongoDB connection

    keyword
        the input keyword initially fetched from the CLI

    Returns
    -------
    str
        a JSON format of the data fetched from the queried MongoDB object
    """
    if keyword == "":
        return to_json([])

    keyword_lower = keyword.lower()
    keyword_cap = keyword.capitalize()

    results = connection.db.news.find(
        {
            "$or": [
                { "title": {"$regex": ".*" + keyword_lower + ".*"} },
                { "title": {"$regex": ".*" + keyword_cap + ".*"} },
                { "article_text": {"$regex": ".*" + keyword_lower + ".*"} },
                { "article_text": {"$regex": ".*" + keyword_cap + ".*"} }
            ]
        }
    )

    news_articles = [ result for result in results ]
    return to_json(news_articles)

def inster_to_db(connection: PyMongo, item: dict) -> None:
        """
        Inserts an item into the MongoDB collection.

        Parameters
        ----------
        conncetion
            the MongoDB connection
        
        item
            the dictionary that contains the yielded item from scraping a news article.
        
        Returns
        -------
        object
            an instance of the class MongoDBPipeline 
        """
        connection.db.news.insert_one(dict(item))