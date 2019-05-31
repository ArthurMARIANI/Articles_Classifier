#!/usr/bin/env python
#! export OBJC_DISABLE_INITIALIZE_FORK_SAFETY = YES
import time
'''
Here is the configuration of the several path and the mode we want to use
'''
FOLDER = "data/"
path = {
    "article_list": FOLDER + "topicdata.txt",
    "json_result": FOLDER + "articles.json",
    "stopwords_folder": "stopwords",
    "json_topics": FOLDER + "topics.json"
}
debug = False
iterations = 1
start_time = time.time()
keywords_to_extract = 20
language = 'fr'
