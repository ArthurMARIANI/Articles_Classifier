#! /usr/bin/env python3
import argparse
import json
import time
import os

from models.article import Article

import config
from crawler import Crawler
from tools.utils import Utils
import multiprocessing as mp
import queue
from collections import OrderedDict
from operator import itemgetter
import itertools

crawler = Crawler()
utils = Utils()
manager = mp.Manager()

articles = []
topics = {}

def run(args):
    queue = manager.Queue()
    pool = mp.Pool(processes=multiprocessing.cpu_count())
    articles_list = utils.filesmanager.read(args.filename).readlines()
    if args.url:
        articles_list = [args.url]
    config.iterations = min(args.number, len(articles_list))
    for i in range(config.iterations):
        article_url = articles_list[i]
        pool.apply_async(
            processRequest, 
            args=(queue, i, article_url), 
            callback=processTreatment)
    pool.close()
    pool.join()
    sortedtopics = OrderedDict(
        sorted(topics.items(), key=itemgetter(1), reverse=True))
    x = itertools.islice(sortedtopics.items(), 0, int(args.topics))
    total = 0
    for key, value in x:
        total += value
        print(key, value)
    print('-------')
    print(str(total) + '/' + str(args.number))
    utils.filesmanager.write(
        articles, config.path['json_result'], True)


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
            url=Utils.cleanUrl(res.url),
            status=res.status_code
        )
        if article.status == 200:
            article = crawler.crawl(article, res)
            if hasattr(article, 'url_categories') and article.url_categories:
                cat = article.url_categories
                if not cat in topics:
                    topics[cat] = 1
                else :
                    topics[cat] += 1 

        articles.append(article.asJSON())
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
