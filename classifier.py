from operator import itemgetter

class Classifier(object):
    def __init__(self):
        self.topics = {}
        self.keywords = {}
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

    def appendKeyword(self, keyword, topic):
        if topic in self.topics:
            if keyword in self.keywords:
                self.keywords[keyword]['occurencies'] = self.keywords[keyword]["occurencies"]+1
                if topic in self.keywords[keyword]:
                    self.keywords[keyword][topic] += 1
                else:
                    self.keywords[keyword][topic] = 1
            else: 
                self.keywords[keyword] = {"occurencies":1}
                if topic in self.keywords[keyword]:
                    self.keywords[keyword][topic] += 1
                else:
                    self.keywords[keyword][topic] = 1

    def extractTopics(self, articles, n_keywords):
        for article in articles:
            if article and 'keywords' in article and article['keywords']:
                article['keywords'] = {keyword: article['keywords'][keyword]
                            for keyword in list(article['keywords'])[:int(n_keywords)]}
                if article and article['topic']:
                    self.appendTopic(article['topic'])

    def extractTopicsFromKeywords(self, articles):
        for article in articles:
            if article and 'topic' in article:
                for keyword in article['keywords']:
                    self.appendKeyword(keyword, article['topic'])
            elif article and 'keywords' in article:
                self.not_labeled.append(article)
                
    def filterTopics(self, n_topics):
        topics = sorted(
            [[k, v['occurencies']] for k, v in self.topics.items()],
             key=itemgetter(1), reverse=True)[:int(n_topics)]
        self.topics = {topic: self.topics[topic] for topic, number in topics}

        
    def normalizeKeywords(self):
        for keyword in self.keywords:
            occurencies = self.keywords[keyword]["occurencies"]
            del self.keywords[keyword]["occurencies"]
            for topic in self.keywords[keyword]:
                    self.keywords[keyword][topic] /= occurencies
      
    def predictTopic(self, articles):
        for article in articles:
                article_topics = {}
                if article and 'keywords' in article and article['keywords']:
                    for keyword in article['keywords']:
                        if keyword in self.keywords:
                            for topic in self.keywords[keyword]:
                                article_topics[topic] = round(self.keywords[keyword][topic]*article['keywords'][keyword],2)
                    topic = sorted(
                        [[topic, weight] for topic, weight in article_topics.items()],
                        key=itemgetter(1), reverse=True)

                    # print('-----')
                    # print(article['title'])
                    # print('------')
                    # for keyword in article['keywords']:
                    #     print(keyword)
                    # print('-----')
                    # for t in topic:
                    #     print(t[1], t[0])
                    if topic:
                        article['predicted_topic'] = topic[0][0]

    def score(self, articles):
        good = 0
        wrong = 0
        for article in articles:
            if article and 'topic' in article and 'predicted_topic' in article:
                print(article['topic'], article['predicted_topic'])
                if article['topic'] == article['predicted_topic']:
                    good +=1
                else:
                    wrong +=1
        print('accuracy:', round(good/wrong,2))


