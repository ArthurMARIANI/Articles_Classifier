from bs4 import BeautifulSoup
import re
from extractor import Extractor
from summarizor import Summarizor
from tools.utils import Utils
from tools.monitor import Monitor

monitor = Monitor()

class Article(object):
    '''
    Contains attributes and fonction related to articles 
    [url, website, title, content, author]
    '''

    def __init__(self, url: str, monitor: Monitor, status: int = None
        ):
        self.url:str = url
        self.status:int
        self.website:str
        self.url_categories:list
        self.author:str
        self.content:str = None
        self.title:str = None
        self.words:int
        self.keywords:list
        self.summary:str
        self.index:int

    def extractContent(self, raw, attributes):
        for attribute in attributes:
            func = getattr(Extractor, attribute)
            setattr(self, attribute, func(raw))

    def extractUrl(self, url, attributes):
        for attribute in attributes:
            func = getattr(Extractor, attribute)
            setattr(self, attribute, func(url))

    def summarize(self):
        summarizor = Summarizor(title= self.title, content=self.content)
        summarizor.normalize("title")
        summarizor.normalize("content")
        self.keywords = summarizor.keywords()

    def asJSON(self):

        article = {}
        for attribute in list(self.__dict__):
            article[attribute] = getattr(self, attribute)
        return article
