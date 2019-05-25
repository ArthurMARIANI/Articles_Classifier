import config
from os import path
from tools.filemanager import FilesManager
import nltk
import spacy
from collections import Counter
from tools.utils import Utils
import math
import re

fm = FilesManager()

class Summarizor(object):
   
    def __init__(self, title, content):
        self.stopwords = self.load_stopwords('fr')
        self.title = title
        self.content = content
        self.spacy = spacy.load('fr_core_news_sm')

    def normalize(self, attribute):
        text = getattr(self, attribute)
        if text:
            text = Utils.clean(text)
            result = []
            doc = self.spacy(text)
            for token in doc:
                if not token.is_stop:
                    if token.lemma_ not in self.stopwords and token.lemma_.isalpha():
                        result.append(token.lemma_)
            setattr(self, attribute, result)
        

    def keywords(self):
        title_keywords = self.getKeywords(self.title)
        content_keywords = self.getKeywords(self.content)
        if title_keywords and content_keywords:
            keywords = Utils.merge_two_dicts(title_keywords[0], content_keywords[0])
            keywords = Utils.sortDictionary(keywords)
            return Utils.normalize(keywords, title_keywords[1]+content_keywords[1])
        else:
            return None

    def getKeywords(self, text):
        """
        get the most used keywords
        """
        if text:
            NUM_KEYWORDS = 20

            freq = {}
            num_words = len(text)
            for word in text:
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1

            min_size = min(NUM_KEYWORDS, len(freq))
            keywords = sorted(freq.items(),
                            key=lambda x: (x[1], x[0]),
                            reverse=True)
            keywords = keywords[:min_size]
            keywords = dict((x, y) for x, y in keywords)

            total = 0
            
            for k in keywords:
                articleScore = keywords[k]**20
                score = round(math.log(articleScore*len(keywords)/math.log(num_words)))

                total += score
                keywords[k] = score
            return [dict(keywords), total]
        else:
            return None

    def load_stopwords(self, language):
        stopwords = set()
        with fm.read(path.join(config.path['stopwords_folder'],
                                         'stopwords-{}.txt'.format(language))) as f:
            stopwords.update(set([w.strip() for w in f.readlines()]))
        return stopwords
