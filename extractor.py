from bs4 import BeautifulSoup
import re
import string
from tools.utils import Utils

class Extractor(object):

    @staticmethod
    def website(url):
        parsed_url = url.split("/")
        website = parsed_url[0]
        return website

    @staticmethod
    def url_categories(url):
        parsed_url = url.split("/")
        url_categories = []
        for i in range(len(parsed_url)-1):
            url_categories.append(parsed_url[i+1])
        return url_categories

    @staticmethod
    def title(raw):
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
    def author(raw):
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
    def content(raw):
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
        if content:
            content_text = '-'.join(content)
            return content_text
        else:
            return None
