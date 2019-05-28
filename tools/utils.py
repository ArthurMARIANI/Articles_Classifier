import string
import json
from pygments import formatters, highlight, lexers
import re
import unidecode
import math
import config
import nlp_config

from os import path

from tools.filemanager import FilesManager

class Utils(object):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.filesmanager = FilesManager()

    @staticmethod
    def cleaner(elements: list):
        """
        Extract the title of the article with this hierarquy : 
        1. In metadata
        2. Reading H1 tags
        """

        cleaned = []
        if elements:
            for element in elements:
                [s.extract() for s in element('i')]
                [s.extract() for s in element('a')]

                content = element.text
                content = content.replace("\n", '')
                content = content.replace("\r", '')
                    
                cleaning_content = content
                for c in string.punctuation:
                    cleaning_content = cleaning_content.replace(c, "")
                if(cleaning_content.split()):
                    cleaned.append(content)

            if cleaned:
                return cleaned
        return None
    
    @staticmethod
    def checkLength(content):
        if content:
            words = 0
            for paragraph in content:
                words += len(paragraph.split())
            return words
        else:
            return 0

    @staticmethod
    def printJson(content):
        colorful_json = highlight(
            json.dumps(
                obj=content,
                indent=2),
            lexers.JsonLexer(),
            formatters.TerminalFormatter()
        )
        print(colorful_json)

    @staticmethod
    def merge_two_dicts(x, y):
        original_value = 0
        for value in x:
            if value in y:
                original_value = y[value]
            y[value] = x[value] + original_value
        return y

    @staticmethod
    def sortDictionary(dictionary):
        dic:dict = {}
        for key, value in sorted(dictionary.items(),reverse=True, key=lambda item: item[1]):
            dic.update({key:value})
        return dic

    @staticmethod
    def isWord(text):
        if text in nlp_config.rejected:
            text = False
        if (text in nlp_config.synonimous):
            text = nlp_config.synonimous[text]
        if text:
            pattern = re.compile(
                r"([0-9])|(\.)|(\-)|(\s+)")
            if not pattern.search(text) and text and len(text)>3:
                return text
            else:
                return False

        #print(re.match(r"l'", '', text))
        #print(re.match("\.\.\.", "", text))



    @staticmethod
    def clean(text):
        text = text.lower()
        text = re.sub(r"d'", '', text)
        text = re.sub(r"l'", '', text)
        text = re.sub("\.\.\.", "", text)        
        text = text.translate(str.maketrans(' ', ' ', string.punctuation))
        text = unidecode.unidecode(text)
        return text

    @staticmethod
    def cleanUrl(text):
        text = re.sub(r"http://", '', text)
        text = re.sub(r"https://", '', text)
        text = re.sub(r"www.", '', text)
        return text

    @staticmethod
    def normalize(obj, total):
        for e in obj:
            val = round(obj[e]/total*100,1)
            if val > 1:
                obj[e] = round(math.log(val), 1)
        return dict(obj)

    def load_stopwords(self, language):
        stopwords = set()
        with self.filesmanager.read(path.join(config.path['stopwords_folder'],
                                            'stopwords-{}.txt'.format(language))) as f:
            stopwords.update(set([w.strip() for w in f.readlines()]))
        return stopwords
