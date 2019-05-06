'''
This is the main file, the one we are calling and which is launching the crawler
'''

import requests
from tools.crawler import Crawler
import sys
import config
from models.article import Article
from pygments import highlight, lexers, formatters
import json

def main():
    '''
    Launcher of the app, should be launch using main.py *number of articles to scrap* *mode(optional, use d for debug)*
    '''
    mode = None
    if len(sys.argv) > 2:
        mode = sys.argv[2]
    if sys.argv[1].isdigit():
        Crawler(int(sys.argv[1]), mode)
    else:
        article = Crawler.getArticle(sys.argv[1], True)
        colorful_json = highlight(
            json.dumps(article, indent=2), lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)
main()
