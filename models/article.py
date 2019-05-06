from bs4 import BeautifulSoup
import re
from tools.extractor import Extractor
from tools.utils import Utils
from tools.monitor import Monitor

class Article(object):
    '''
    Contains attributes and fonction related to articles 
    [url, website, title, content, author]
    '''

    def __init__(self, url:str = None, raw:str = None) :
        raw = BeautifulSoup(raw.text, 'html.parser')
        self.url = url
        self.runExtractors(raw)

    def runExtractors(self, raw):

        for method in dir(Extractor):
            if method.startswith("extract"):
                func = getattr(Extractor, method)
                attribute = re.sub('extract', '', method).lower()
                setattr(self, attribute, func(raw))

    def asJSON(self):
        '''
        Returning a json version of the object / define of return scheme the attributes you want to integrate
        '''

        article = {}
        for attribute in list(self.__dict__):
            article[attribute] = getattr(self, attribute)
        return article
