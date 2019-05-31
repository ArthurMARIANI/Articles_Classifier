import requests
from tools.utils import Utils
import config
import json
from models.article import Article
from extractor import Extractor

from bs4 import BeautifulSoup

utils = Utils()
extractor = Extractor()

class Crawler(object):
            
    def parseArticle(self, article):
        raw = BeautifulSoup(article.raw, 'html.parser')
        setattr(article, 'title', extractor.extractTitle(raw))
        setattr(article, 'author', extractor.extractAuthor(raw))
        setattr(article, 'content', extractor.extractContent(raw))
        if hasattr(article, 'content'):
            setattr(article, 'words', Utils.checkLength(article.content))
            setattr(article, 'topic', extractor.extractTopic(article.url))

            if hasattr(article, 'topic'):
                print(article.topic)
            else :
                print(article.url)
        
        return article
    
    def requestArticle(self, url, index):
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

        return Article(
            url= res.url,
            status=res.status_code,
            raw = res.text,
            index = index
        )
        
