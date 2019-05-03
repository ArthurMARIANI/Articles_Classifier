from bs4 import BeautifulSoup
import re

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
        for method in dir(self):
            if(method.startswith("extract")):
                func = getattr(self, method)
                attribute = re.sub('extract', '', method).lower()
                print(attribute)
                try:
                    setattr(self, attribute, func(raw))
                except:
                    return None
    
    def asJSON(self):
        '''
        Returning a json version of the object / define of return scheme the attributes you want to integrate
        '''

        article = {}
        for attribute in list(self.__dict__):
            article[attribute] = getattr(self, attribute)

        return article


# add extractor using as format: extractNameofAttribute(self, raw)

    def extractTitle(self, raw):
        '''
        Extracting from metadata the title of the page
        '''
        return raw.title.string