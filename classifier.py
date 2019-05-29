from operator import itemgetter

class Classifier(object):
    def __init__(self):
        self.topics = {}
        self.not_labeled = []

    def appendTopic(self, topic):
        if topic in self.topics:
            self.topics[topic] = {
                "occurencies": self.topics[topic]["occurencies"]+1
            }
        else :
            self.topics[topic] = {
                "occurencies" : 1
            }

    def extractTopicKeys(self, articles):
        for article in articles:
            if article and article['topic']:
                self.appendTopic(article['topic'])
                for keyword in article['keywords']:
                    topic = self.topics[article['topic']]
                    if keyword in topic:
                        topic[keyword] = {
                            "cumulated_score": topic[keyword]['cumulated_score']+article['keywords'][keyword],
                            "appearing_score": topic[keyword]['appearing_score']+1
                        }
                    else:
                        topic[keyword] = {
                            "cumulated_score": article['keywords'][keyword],
                            "appearing_score": 1
                        }
            else:
                if 'keywords' in article:
                    self.not_labeled.append(article)

    def filterTopics(self, n_topics):
        topics = sorted(
            [[k, v['occurencies']] for k, v in self.topics.items()],
             key=itemgetter(1), reverse=True)[:int(n_topics)]
        self.topics = {topic: self.topics[topic] for topic, number in topics}


        
    def normalizeTopics(self):
        for topic in self.topics:
            occurencies = self.topics[topic]["occurencies"]
            for keyword in self.topics[topic]:
                if keyword is not 'occurencies':
                    cumulated = self.topics[topic][keyword]['cumulated_score']
                    appearing = self.topics[topic][keyword]['appearing_score']
                    proportion_appearing = (appearing/occurencies*10)
                    self.topics[topic][keyword] = round(proportion_appearing * cumulated, 1)

    def predictTopic(self):
        for article in self.not_labeled:
            article_topics = {}
            for keyword in article['keywords']:
                for topic in self.topics:
                    if keyword in self.topics[topic]:
                        article_topics[topic] = self.topics[topic][keyword]
            topic = sorted(
                [[topic, weight] for topic, weight in article_topics.items()],
                key=itemgetter(1), reverse=True)
            print('-----')
            print(article['title'])
            for t in topic:
                print(t[0], t)
