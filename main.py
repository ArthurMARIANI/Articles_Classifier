#! /usr/bin/env python3

import json
import config.config as config
from crawler import Crawler
from models.article import Article
from summarizor import Summarizor
from classifier import Classifier
from tools.utils import Utils
from collections import OrderedDict
import multiprocessing as mp
import queue
import os


utils = Utils()
manager = mp.Manager()
crawler = Crawler()
classifier = Classifier()
summarizor = Summarizor()

articles = []


def run(args):
    existing_articles = 0
    json_file = open(config.path['json_result']).read()
    if json_file and not args.rebuild:
        previous_articles = json.loads(json_file)
        existing_articles = previous_articles['number']
        for json_article in previous_articles['articles']:
            article = Article(
                url=json_article['url'],
                status=json_article['status'],
            )
            if 'topic' in json_article:
                article.topic: list = json_article['topic']
            if 'title' in json_article:
                article.title: str = json_article['title']
            if 'keywords' in json_article:
                article.keywords: list = json_article['keywords']
            articles.append(article)

    queue = manager.Queue()
    pool = mp.Pool(processes=mp.cpu_count())
    with open(args.filename, 'r') as articles_list:
        articles_list = articles_list.readlines()
        articles_list = list(OrderedDict.fromkeys(articles_list))
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
            with open(os.path.abspath(os.curdir)+'/'+config.path['json_result'], 'w') as f:
                json.dump({"number": target, "articles": json_articles},
                          f, ensure_ascii=False)

    classifier.run(
        articles=articles[:args.number],
        n_keywords=args.n_keywords,
        n_topics=args.n_topics)


def processRequest(queue, index, article_url):
    article = crawler.requestArticle(
        url=article_url,
        index=index
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
        if not config.debug:
            utils.printJson(article.asJSON())
        delattr(article, 'index')
        articles.append(article)
        break


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Articles Classifier"
    )

    parser.add_argument("-n",
                        help="number of articles you want to scrap",
                        dest="number",
                        type=int,
                        default=1,
                        required=False
                        )

    parser.add_argument("-d",
                        help="activate debug mode",
                        action="store_const",
                        dest="debug",
                        const=True,
                        default=False,
                        required=False
                        )

    parser.add_argument("-r",
                        help="rebuild previous database",
                        action="store_const",
                        dest="rebuild",
                        const=True,
                        default=False,
                        required=False
                        )

    parser.add_argument("-t",
                        help="number of topics expected",
                        dest="n_topics",
                        default=10,
                        required=False
                        )

    parser.add_argument("-k",
                        help="number of keywords to use",
                        dest="n_keywords",
                        default=10,
                        required=False
                        )

    parser.add_argument("-list",
                        help="name of txt file you want to process",
                        dest="filename",
                        type=str,
                        default=config.path['article_list'],
                        required=False
                        )

    parser.set_defaults(func=run)
    args = parser.parse_args()
    config.debug = args.debug
    args.func(args)


if __name__ == "__main__":
    main()
