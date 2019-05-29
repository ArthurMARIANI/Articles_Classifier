class Classifier(object):
    def __init__(self):
        self.topics = {}

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
        print(articles)
        for article in articles:
            pass
            # if article['topic'] and article['topic'] in self.topics:
            #     for keyword in article['keywords']:
            #         topic = self.topics[article['topic']]
            #         if keyword in topic:
            #             topic[keyword] = {
            #                 "cumulated_score": topic[keyword]['cumulated_score']+article['keywords'][keyword],
            #                 "appearing_score": topic[keyword]['appearing_score']+1
            #             }
            #         else:
            #             topic[keyword] = {
            #                 "cumulated_score": article['keywords'][keyword],
            #                 "appearing_score": 1
            #             }

    def normalizeTopics(self):
        for topic in self.topics:
            occurencies = self.topics[topic]["occurencies"]
            for keyword in self.topics[topic]:
                if keyword is not 'occurencies':
                    cumulated = self.topics[topic][keyword]['cumulated_score']
                    appearing = self.topics[topic][keyword]['appearing_score']
                    mean_weight = (cumulated/appearing)
                    proportion_appearing = (appearing/occurencies)
                    self.topics[topic][keyword] = round(proportion_appearing, 1)
        print(self.topics)