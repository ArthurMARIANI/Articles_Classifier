#!/usr/bin/env python
'''
Here is the configuration of the several path and the mode we want to use
'''


path = {
    "article_list": "topicdata.txt", #list of articles (the one given)
    "json_result": "articles.json", #the json where to export the result
    "stopwords_folder": "stopwords"
}
mode = "test" #test or full
cache = 1

sentence_importance  = {
    0: 0,
    0.1: 0.17,
    0.2: 0.23,
    0.3: 0.14,
    0.4: 0.08,
    0.5: 0.05,
    0.6: 0.04,
    0.7: 0.06,
    0.8: 0.04,
    0.9: 0.04,
    1: 0.15,
    1.1: 0
}