#! /usr/bin/env python3
import argparse
import json
import time
import os

from models.article import Article

import config
from crawler import Crawler
from classifier import Classifier
from tools.utils import Utils
import multiprocessing as mp
import queue
from collections import OrderedDict
from operator import itemgetter
import itertools
import multiprocessing
import numpy as np

utils = Utils()
manager = mp.Manager()
crawler = Crawler()
classifier = Classifier()

def run(args):
    queue = manager.Queue()
    existing_articles = crawler.existing_articles
    pool = mp.Pool(processes=multiprocessing.cpu_count())
    articles_list = utils.filesmanager.read(args.filename).readlines()
    target = min(args.number, len(articles_list))
    config.iterations = target - existing_articles
    if config.iterations > 0:
        if args.url:
            articles_list = [args.url]
        for i in range(config.iterations):
            index = i+existing_articles
            article_url = articles_list[index]
            pool.apply_async(
                processRequest, 
                args=(queue, index, article_url),
                callback=processTreatment)
        pool.close()
        pool.join()
    classifier.extractTopics(crawler.articles, args.keywords)
    classifier.filterTopics(args.topics)
    classifier.extractTopicsFromKeywords(crawler.articles)
    classifier.normalizeKeywords()
    classifier.predictTopic(crawler.articles)
    classifier.score(crawler.articles)
    utils.filesmanager.write({"number": target,
                              "articles": crawler.articles
                              }, 
                              config.path['json_result'], True
        )

def processRequest(queue, i, article_url):
    res = crawler.getArticle(article_url)
    element = {
        'index':i,
        'res':res
    }
    queue.put(element)
    return queue

def processTreatment(queue):
    while True:
        element = queue.get()
        res = element['res']
        article = Article( 
            index=element['index'],
            url=res.url,
            status=res.status_code
        )
        if article.status == 200:
            crawler.crawl(article, res)
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
        dest = "topics", 
        default = 10,
        required = False
    )

    parser.add_argument("-k", 
        help = "number of keywords to use",
        dest = "keywords", 
        default = 10,
        required = False
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-url",
        help = "url to scrap",
        dest="url",
        type = str,
        required = False
    )

    group.add_argument("-list",
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
