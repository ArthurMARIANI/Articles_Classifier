from operator import itemgetter
import itertools
from tools.utils import Utils

class Classifier(object):
    def __init__(self):
        self.topics = {}
        self.keywords = {}
        self.not_labeled = []


    def run(self, articles, n_keywords=False, n_topics=False):
        self.articles = articles
        scores = []
        for n_topics in range(5, 14):
            for n_keywords in range(2,10):
                self.extractTopics(n_topics)
                self.extractKeywords(n_keywords)
                self.normalizeKeywords(n_keywords)
                self.predictTopic(n_keywords)
                print('keywords: ',n_keywords, 'n_topics: ',n_topics)
                print(self.score())
                print('------')
                scores.append(
                    {"score":self.score(),
                    "n_keywords":n_keywords,
                    "n_topics":n_topics}
                    )
        self.optimise(scores)

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
        print(best)

    def appendTopic(self, topic):
        if topic in self.topics:
            self.topics[topic] = {
                "occurencies": self.topics[topic]["occurencies"]+1
            }
        else :
            self.topics[topic] = {
                "occurencies" : 1
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
        for article in self.articles:
            if 'topic' in article:
                self.appendTopic(article['topic'])
        topics = sorted(
            [[k, v['occurencies']] for k, v in self.topics.items()],
             key=itemgetter(1), reverse=True)[:int(n_topics)]
        self.topics = {topic: self.topics[topic] for topic, number in topics}
                    
    def extractKeywords(self, n_keywords):
        for article in self.articles:
            if article and 'topic' in article and 'keywords' in article and article['keywords']:
                for keyword in dict(itertools.islice(article['keywords'].items(), 1, n_keywords+1)):
                    self.appendKeyword(keyword, article['topic'])
            elif article and 'keywords' in article:
                self.not_labeled.append(article)

    def normalizeKeywords(self, n_keywords):
        for keyword in self.keywords:
            if self.keywords[keyword]:
                keywords = dict(itertools.islice(
                    self.keywords[keyword].items(), 1, n_keywords))
                occurencies = 0
                for topic in keywords:
                    occurencies += self.keywords[keyword][topic]
                for topic in keywords:
                    self.keywords[keyword][topic] = self.keywords[keyword][topic]/occurencies

    def predictTopic(self, n_keywords):
        for article in self.articles:
            article_topics = {}
            if article and 'topic' in article and 'keywords' in article and article['keywords']:
                keywords = dict(itertools.islice(
                    article['keywords'].items(), 1, n_keywords))
                for keyword in keywords:
                    if keyword in self.keywords:
                        for topic in self.keywords[keyword]:
                            article_topics[topic] = round(self.keywords[keyword][topic]*article['keywords'][keyword],2)
                topic = sorted(
                    [[topic, weight] for topic, weight in article_topics.items()],
                    key=itemgetter(1), reverse=True)
                if topic:
                    article['predicted_topic'] = topic[0][0]
                    #print(article['title'], article['predicted_topic'])

    def score(self):
        good = 0
        wrong = 0
        for article in self.articles:
            if article and 'topic' in article and 'predicted_topic' in article:
                if article['topic'] == article['predicted_topic']:
                    good +=1
                else:
                    wrong +=1

        accuracy = 1
        if wrong != 0:
            accuracy = round(good/(good+wrong), 3)
        return accuracy
        


