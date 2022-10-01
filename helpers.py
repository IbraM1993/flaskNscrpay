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
    print(keyword)
    results = connection.db.news.find(
        {
            "$or": [
                { "title": {"$regex": ".*" + keyword + ".*"} },
                { "article_text": {"$regex": ".*" + keyword + ".*"} }
            ]
        }
    )

    news_articles = [ result for result in results ]
    return to_json(news_articles)