from operator import itemgetter
import itertools
from tools.utils import Utils
import math


class Classifier(object):
    def __init__(self):
        self.topics = {}
        self.keywords = {}
        self.train = []
        self.test = []
        self.not_labeled = []
        self.scores = []

    def run(self, articles, n_keywords=False, n_topics=False):
        print('CLASSIFIER')
        self.train = articles[:int(len(articles) * 0.8)-1]
        self.test = articles[:int(len(articles) * -0.2)-1]
        for n_topics in range(15, 16):
            for n_keywords in range(2, 3):
                self.extractTopics(n_topics)
                for topic in self.topics:
                    print(topic)
                self.extractKeywords(n_keywords)
                self.predictTopic(n_keywords)
                self.score(n_keywords, n_topics)
        self.optimise(self.scores)

    def appendTopic(self, topic):
        if topic in self.topics:
            self.topics[topic] = {
                "occurencies": self.topics[topic]["occurencies"]+1
            }
        else:
            self.topics[topic] = {
                "occurencies": 1
            }

    def appendKeyword(self, keyword, topic):
        if topic in self.topics:
            if keyword in self.keywords:
                if topic in self.keywords[keyword]:
                    self.keywords[keyword][topic] += 1
                else:
                    self.keywords[keyword][topic] = 1
            else:
                self.keywords[keyword] = {}

    def extractTopics(self, n_topics):
        self.topics = {}
        for article in self.train:
            if article and hasattr(article, 'keywords'):
                if hasattr(article, 'topic') and article.topic is not None:
                    self.appendTopic(article.topic)
                    print(article.topic)
                    print(article.url)
                else:
                    self.not_labeled.append(article)
        topics = sorted(
            [[k, v['occurencies']] for k, v in self.topics.items()],
            key=itemgetter(1), reverse=True)[:int(n_topics)]
        self.topics = {topic: self.topics[topic] for topic, number in topics}

    def extractKeywords(self, n_keywords):
        self.keywords = {}
        for article in self.train:
            if hasattr(article, 'keywords') and article.keywords and hasattr(article, 'topic'):
                for keyword in dict(itertools.islice(article.keywords.items(), 1, n_keywords)):
                    self.appendKeyword(keyword, article.topic)

    def predictTopic(self, n_keywords):
        for article in self.test:
            article_topics = {}
            if hasattr(article, 'status') and article.status == 200 and hasattr(article, 'keywords') and article.keywords:
                keywords = dict(itertools.islice(
                    article.keywords.items(), 1, n_keywords))
                for keyword in keywords:
                    if keyword in self.keywords:
                        for topic in self.keywords[keyword]:
                            weight = article.keywords[keyword]
                            article_topics[topic] = round(
                                self.keywords[keyword][topic]*math.log(weight), 2)
                topic = sorted(
                    [[topic, weight]
                        for topic, weight in article_topics.items()],
                    key=itemgetter(1), reverse=True)
                if topic:
                    article.predicted_topic = topic[0][0]
                else:
                    article.predicted_topic = None
            else:
                pass

    def score(self, n_keywords, n_topics):
        good = 0
        wrong = 0
        for article in self.test:
            if hasattr(article, 'topic') and hasattr(article, 'predicted_topic'):
                if article.topic == article.predicted_topic:
                    good += 1
                else:
                    wrong += 1
        accuracy = 1
        if wrong != 0:
            accuracy = round(good/(good+wrong), 3)

        self.scores.append(
            {"score": accuracy,
             "n_keywords": n_keywords,
             "n_topics": n_topics}
        )

    def optimise(self, scores):
        scores = sorted(
            [[score['score'], score['n_keywords'], score['n_topics']]
                for score in scores],
            key=itemgetter(0), reverse=True)

        best = {
            "score": scores[0][0],
            "n_keywords": scores[0][1],
            "n_topics": scores[0][2]
        }
        print('\n')
        print('BEST')
        print('----')
        print(best['score'])
        print('keywords: ', best['n_keywords'], 'n_topics: ', best['n_topics'])
        print('----')
