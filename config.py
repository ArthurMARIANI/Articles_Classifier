#!/usr/bin/env python
#! export OBJC_DISABLE_INITIALIZE_FORK_SAFETY = YES
import time
'''
Here is the configuration of the several path and the mode we want to use
'''

path = {
    "article_list": "topicdata.txt", #list of articles (the one given)
    "json_result": "articles.json", #the json where to export the result
    "stopwords_folder": "stopwords",
    "json_topics": "topics.json"
}
debug = False 
iterations = 1
start_time = time.time()