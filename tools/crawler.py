import requests
import time
from models.article import Article
from files.filemanager import FilesManager
from pygments import highlight, lexers, formatters
import config
import json
from tools.monitor import Monitor

fm = FilesManager()
monitor = Monitor()

class Crawler(object):

    def __init__(self, number:int = 1, mode=None):
        '''
        The Crawler will request every url present on the article list file in config send the content into the Articles model for the treatment. It needs as input the number of urls that you want to read
        '''
        self.mode = mode
        self.number = number
        article_list = fm.read(config.path['article_list'])
        self.read_list(article_list)

    def read_list(self, article_list: list):
        ''' 
        Looping over the article_list file given as argument
        '''
        start_time = time.time()
        articles = []

        i = 0
        while i < self.number: 
            elapsed_time = round(time.time() - start_time,1)
            monitor.appendAdvance(i+1, self.number, elapsed_time)
            url = article_list.readline()
            article = self.getArticle(url)
            print(i)
            if article:
                monitor.appendWords(article.words)
                articles.append(article.asJSON())
            else:
                monitor.appendWords(None)
            if self.mode != "d":
                monitor.updatePrint()
            fm.write(articles, config.path['json_result'],True)
            i+=1
        return True

    
    @staticmethod
    def getArticle(url, raw:bool = False):
        a = 0
        try:
            req = requests.get("http://"+url, allow_redirects=True)
            status = req.status_code
            monitor.appendStatus(status)
            if status == 200:
                article = Article(url, req)
                print(article)
                if raw:
                    setattr(article, 'raw', str(req.text))
                    fm.write(article.asJSON(), config.path['json_result'], True)
                return article
        except:
            time.sleep(0.5)
        
