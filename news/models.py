from django.db import models
from HyperNews_Portal.settings import NEWS_JSON_PATH
import datetime
import json


def get_news_articles():
    with open(NEWS_JSON_PATH, "r") as json_file:
        return json.load(json_file)


def get_news_article(link):
    for article in get_news_articles():
        if article["link"] == link:
            return article
    return None


def get_news_articles_sorted_by_date(newer_first=True):
    return __sort_articles_by_date(get_news_articles(), newer_first)


def add_news_article(title, text):
    articles = get_news_articles()
    articles.append({"created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "title": title,
                     "text": text,
                     "link": max(articles, key=lambda a: a['link'])['link'] + 1})
    __save_articles_to_file(articles, NEWS_JSON_PATH)


def __save_articles_to_file(articles, db_path):
    with open(db_path, 'w') as json_file:
        json.dump(articles, json_file)


def __sort_articles_by_date(articles, newer_first=True):
    articles.sort(key=lambda v: v["created"])
    if newer_first:
        articles.reverse()
    sorted_articles = {}

    for article in articles:
        sorted_articles.setdefault(article["created"][:10], []).append(article)

    return sorted_articles.items()
