from extractor import Extractor
from summarizor import Summarizor
from tools.utils import Utils

class Article(object):
    '''
    Contains attributes and fonction related to articles 
    [url, website, title, content, author]
    '''

    def __init__(self, url: str, status:int, index:int):
        self.index = index
        self.url:str = url
        self.status:int = status
        self.website:str
        self.topic:list = None
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
        summarizor = Summarizor(
            title=self.title, content=self.content)
        summarizor.normalize("title")
        summarizor.normalize("content")
        self.keywords = summarizor.keywords()

    def asJSON(self):

        article = {}
        for attribute in list(self.__dict__):
            article[attribute] = getattr(self, attribute)
        return article
