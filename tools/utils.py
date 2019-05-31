import string
import json
from pygments import formatters, highlight, lexers
import re
import unidecode
import math
import config.config as config
import config.nlp_config as nlp_config

from os import path


class Utils(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

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

    @staticmethod
    def cleanText(text):
        from spacy.lang.fr import French
        spacy = French()
        stopwords = stopwords = set()
        with open(path.join(config.path['stopwords_folder'],
                            'stopwords-{}.txt'.format(config.language))) as f:
            stopwords.update(set([w.strip() for w in f.readlines()]))
        if text:
            text = text.lower()
            text = re.sub(r"d'", '', text)
            text = re.sub(r"l'", '', text)
            text = re.sub(r"le'", '', text)
            text = re.sub("\.\.\.", "", text)
            text = text.translate(str.maketrans(' ', ' ', string.punctuation))
            text = unidecode.unidecode(text)
            result = []
            doc = spacy(text)
            for token in doc:
                if not token.is_stop:
                    if token.lemma_ not in stopwords and token.lemma_.isalpha():
                        result.append(token.lemma_)
            return result

    @staticmethod
    def split(delimiters, string, maxsplit=0):
        import re
        regexPattern = '|'.join(map(re.escape, delimiters))
        return re.split(regexPattern, string, maxsplit)

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
        dic: dict = {}
        for key, value in sorted(dictionary.items(), reverse=True, key=lambda item: item[1]):
            dic.update({key: value})
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
            if not pattern.search(text) and text and len(text) > 3 and len(text) < 10:
                return text
            else:
                return False

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
            val = round(obj[e]/total*100, 1)
            if val > 1:
                obj[e] = round(math.log(val), 1)
        return dict(obj)

    @staticmethod
    def load_stopwords(language):
        stopwords = set()
        with open(path.join(config.path['stopwords_folder'],
                            'stopwords-{}.txt'.format(language))) as f:
            stopwords.update(set([w.strip() for w in f.readlines()]))
        return stopwords
