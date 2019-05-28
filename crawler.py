import requests
from tools.utils import Utils
from models.article import Article
import time
import config

from bs4 import BeautifulSoup

utils = Utils()

class Crawler(object):

    def crawl(self, article, res):

        raw = BeautifulSoup(res.text, 'html.parser')
        article.extractContent(raw, attributes=[
            "title",
            "author",
            "content"
        ])
        if article.content:
            article.words = Utils.checkLength(article.content)
            article.extractUrl(article.url,
                                attributes=[
                                    "website",
                                    "url_categories",
                                ])
            article.summarize()
            delattr(article, "content")
            if not config.debug:
                Utils.printJson(article.asJSON())
        return article
    
    def getArticle(self, url) -> object:
        url = utils.cleanUrl(url)
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'CHROME_WIN_UA',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }
        res = requests.get(
            url="http://"+url, 
            allow_redirects=True,
            headers=headers
        )
        return res
        
