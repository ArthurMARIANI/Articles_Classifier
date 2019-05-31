from tools.utils import Utils
import re


class Extractor(object):

    @staticmethod
    def extractTopic(url):
        website = Utils.split(['/', '.', '-', 'des', 'du', ], url)[:-1]
        for word in website:
            word = Utils.cleanText(word)
            if word:
                word = Utils.isWord(word[0])
                if word:
                   # print(word)
                    return word
                else:
                    pass
                   # print(website)

    @staticmethod
    def extractTitle(raw):
        title_element = raw.title
        if title_element and title_element.string:
            return title_element.string.lower()
        else:
            titles_text_H1 = [tag.string for tag in raw.find_all('h1')]
            if titles_text_H1:
                titles_text_H1.sort(key=len, reverse=True)
                return titles_text_H1[0]

    @staticmethod
    def extractAuthor(raw):

        ATTRS = ['name', 'rel', 'itemprop', 'class', 'id']
        VALS = ['author', 'byline', 'dc.creator', 'byl']

        for attr in ATTRS:
            for val in VALS:
                match = raw.find(attrs={attr: val})
                if match:
                    return match.string

    @staticmethod
    def extractContent(raw):
        section = raw
        raw.find_all('footer').clear()
        if raw.find('article'):
            section = raw.find('article')
        content = Utils.cleaner(section.find_all("p"))
        if content:
            content_text = '-'.join(content)
            return content_text
