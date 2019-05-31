import config.config as config
from os import path
import math
from tools.utils import Utils


class Summarizor(object):

    def summarizeArticle(self, article):
        title = ''
        if hasattr(article, 'title'):
            title = article.title
        title = Utils.cleanText(title)
        if hasattr(article, 'content'):
            content = Utils.cleanText(article.content)
            title_keywords = self.getKeywords(title)
            content_keywords = self.getKeywords(content)
            if title_keywords and content_keywords:
                keywords = Utils.merge_two_dicts(
                    title_keywords[0], content_keywords[0])
                keywords = Utils.sortDictionary(keywords)
                article.keywords = Utils.normalize(keywords, 4)
        return article

    def getKeywords(self, text):
        if text:
            NUM_KEYWORDS = config.keywords_to_extract
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
                articleScore = math.log((keywords[k]*2)**2)+1
                length = math.log(num_words / len(keywords))+1
                score = articleScore/length

                total += score
                keywords[k] = score
            return [dict(keywords), total]
