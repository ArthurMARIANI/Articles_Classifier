from bs4 import BeautifulSoup
import re
from tools.content_extractor import ContentExtractor
from tools.nlp import Nlp
from urllib.parse import *


class Article(object):
    '''
    Contains attributes and fonction related to articles 
    [url, website, title, content, author]
    '''

    def __init__(self, url:str = None, raw:str = None) :
        raw = BeautifulSoup(raw.text, 'html.parser')
        self.url = url
        self.extractContent(raw)
        self.extractUrl(url)

    def extractUrl(self, url):
        parsed_url = url.split("/")
        website = parsed_url[0]
        url_categories = [parsed_url[1], parsed_url[2]]
        setattr(self, "urls_categories", url_categories)
        setattr(self, "website", website)

    def extractContent(self, raw):
        for method in dir(ContentExtractor):
            if method.startswith("extract"):
                func = getattr(ContentExtractor, method)
                attribute = re.sub('extract', '', method).lower()
                setattr(self, attribute, func(raw))

    def nlp(self):
        """Keyword extraction wrapper
        """

        nlp = Nlp()

        text_keyws = list(nlp.keywords(self.content).keys())
        title_keyws = list(nlp.keywords(self.title).keys())
        keyws = list(set(title_keyws + text_keyws))
        setattr(self, 'keywords', keyws)
        
        summary_sents = nlp.summarize(
            title=self.title, text=self.content, max_sents=5)
        summary = '\n'.join(summary_sents)
        nlp.score()
        setattr(self, 'summary', summary)

    def asJSON(self):
        '''
        Returning a json version of the object / define of return scheme the attributes you want to integrate
        '''

        article = {}
        for attribute in list(self.__dict__):
            article[attribute] = getattr(self, attribute)
        return article
