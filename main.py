#! /usr/bin/env python3
import argparse
import json
import time

from bs4 import BeautifulSoup

import config
from crawler import Crawler
from extractor import Extractor
from models.article import Article
from tools.filemanager import FilesManager
from tools.monitor import Monitor
from tools.utils import Utils

fm = FilesManager("Articles_Classifier")
monitor = Monitor()
crawler = Crawler(
    monitor=monitor
)

def processArticle(article, res, url):
    if(hasattr(res, "text")):
        raw = BeautifulSoup(res.text, 'html.parser')
        article.extractContent(raw,
            attributes=[
                "title",
                "author",
                "content"
            ])

        if article.content:
            article.words = Utils.checkLength(article.content)

        article.extractUrl(url,
            attributes=[
                "website",
                "url_categories",
            ])

        article.summarize()

        delattr(article, "content")
        delattr(article, "author")
    
def run(args):
    articles = []
    start_time = time.time()
    articles_list = fm.read(args.filename)
    for i in range(args.number):
        if args.url: url = args.url
        else: url = articles_list.readline()
        if not url:
            return False
        url = Utils.cleanUrl(url) 
        monitor.clearMonitor()
        monitor.appendUrl(url)
        monitor.appendAdvance(
            advance = i+1, 
            total = args.number, 
            time = round(time.time() - start_time, 1)
        )
        res = crawler.crawl(
            url = url, 
            debug = args.debug
        )
        
        article = Article(
            url=url,
            monitor=monitor
        )

        if(isinstance(res, int)): 
            article.status = res
            monitor.appendWords(None)
        else: 
            processArticle(article, res, url)
            if hasattr(article, 'words'):
                monitor.appendWords(article.words)
            else:
                monitor.appendWords(None)

        article.index = i+1

        if args.debug:
            Utils.printJson(article.asJSON())
        else:
            monitor.updatePrint()

        articles.append(article.asJSON())
        fm.write(articles, config.path['json_result'], True)
    monitor.updatePrint()
    return True

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

    parser.add_argument("-w",
        help = "define each how many iterations you want to write",
        dest="write",
        type = int,
        default = config.cache,
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
    args.func(args)

if __name__ == "__main__":
    main()
