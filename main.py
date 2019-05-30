#! /usr/bin/env python3
import argparse
import json
import os

from models.article import Article

import config
from crawler import Crawler
from summarizor import Summarizor
from classifier import Classifier
from tools.utils import Utils
import multiprocessing as mp
import queue
import multiprocessing

utils = Utils()
manager = mp.Manager()
crawler = Crawler()
classifier = Classifier()
summarizor = Summarizor()

json_file = open('articles.json').read()
if json_file:
    previous_articles = json.loads(json_file)
    existing_articles = previous_articles['number']
    articles = previous_articles['articles']
else:
    existing_articles = 0
    articles = []

def run(args):
    queue = manager.Queue()
    pool = mp.Pool(processes=multiprocessing.cpu_count())  
    articles_list = utils.filesmanager.read(args.filename).readlines()
    target = min(args.number, len(articles_list))
    iterations = target - existing_articles
    if iterations > 0:
        for i in range(iterations):
            index = i+existing_articles
            article_url = articles_list[index]
            pool.apply_async(processRequest, 
                args=(queue, index, article_url),
                callback=processTreatment)
        pool.close()
        pool.join()
        json_articles = []
        for article in articles:
            json_articles.append(article.asJSON())
        utils.filesmanager.write({"number": target,
                                  "articles": json_articles
                                }, 
                                config.path['json_result'], True
        )
    classifier.run( 
        articles = articles[:args.number], 
        n_keywords = args.n_keywords, 
        n_topics = args.n_topics)

def processRequest(queue, index, article_url):
    article = crawler.requestArticle(
        url = article_url, 
        index = index
    )
    queue.put(article)
    return queue

def processTreatment(queue):
    while True:
        article = queue.get()
        if article.status == 200:
            article = crawler.parseArticle(article)
            article = summarizor.summarizeArticle(article)
            delattr(article, 'content')
            delattr(article, 'words')
        delattr(article, 'raw')
        delattr(article, 'index')
        articles.append(article)
        break

def main():
    parser = argparse.ArgumentParser(
        description="Articles Classifier"
    )

    parser.add_argument("-n", 
        help = "number of articles you want to scrap",
        dest = "number",
        type = int,
        default = 1,
        required = False
    )

    parser.add_argument("-d", 
        help = "activate debug mode",
        action = "store_const",
        dest = "debug", 
        const = True, 
        default = False,
        required = False
    )

    parser.add_argument("-t", 
        help = "number of topics expected",
        dest = "n_topics", 
        default = 10,
        required = False
    )

    parser.add_argument("-k", 
        help = "number of keywords to use",
        dest = "n_keywords", 
        default = 10,
        required = False
    )

    parser.add_argument("-list",
        help = "name of txt file you want to process",
        dest="filename",
        type = str,
        default = config.path['article_list'],
        required = False
    )

    parser.set_defaults(func=run)
    args = parser.parse_args()
    config.debug = args.debug
    args.func(args)

if __name__ == "__main__":
    main()
