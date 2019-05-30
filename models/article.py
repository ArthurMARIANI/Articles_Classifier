from extractor import Extractor
from summarizor import Summarizor
from tools.utils import Utils

class Article(object):
    '''
    Contains attributes and fonction related to articles 
    [url, website, title, content, author]
    '''

    def __init__(self, url: str, status:int, index:int, raw:str= None):

        self.index = index
        self.url:str = Utils.cleanUrl(url)
        self.raw:str = raw
        self.status:int = status
        self.website:str
        self.topic:list
        self.predicted_topic:str 
        self.author:str
        self.content:str
        self.title:str
        self.words:int
        self.keywords:list
        self.summary:str
        self.index:int

    def asJSON(self):
        article = {}
        for attribute in list(self.__dict__):
            article[attribute] = getattr(self, attribute)
        return article
