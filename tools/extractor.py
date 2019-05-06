from bs4 import BeautifulSoup
import re
import string
from .utils import Utils

class Extractor(object):

    @staticmethod
    def extractTitle(raw):
        """
        Extract the title of the article with this hierarquy : 
        1. In metadata
        2. Reading H1 tags
        """

        title = None

        title_element = raw.title
        if title_element:
            title = title_element.string.lower()

        else:
            titles_text_H1 = [tag.string for tag in raw.find_all('h1')]
            if titles_text_H1:
                titles_text_H1.sort(key=len, reverse=True)
                title = titles_text_H1[0]

        return title

    @staticmethod
    def extractAuthor(raw):
        """
        Extract the author of the article using multiple combinations of tags attributes/value
        """

        ATTRS = ['name', 'rel', 'itemprop', 'class', 'id']
        VALS = ['author', 'byline', 'dc.creator', 'byl']

        for attr in ATTRS:
            for val in VALS:
                match = raw.find(attrs={attr: val})
                if match:
                    return match.string

    @staticmethod
    def extractWords(raw):
        """
        Extract the Content of the article: 
        1. Excluding Footer
        2. Looking for article Tag
        """
        
        section = raw
        raw.find_all('footer').clear()
        if raw.find('article'):
            section = raw.find('article')
        content = Utils.cleaner(section.find_all("p"))
        words = Utils.checkLength(content)
        return words
        
    @staticmethod
    def extractContent(raw):
        """
        Extract the Content of the article: 
        1. Excluding Footer
        2. Looking for article Tag
        """
        
        section = raw
        raw.find_all('footer').clear()
        if raw.find('article'):
            section = raw.find('article')
        content = Utils.cleaner(section.find_all("p"))
        
        return content
