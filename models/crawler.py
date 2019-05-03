import requests
import time
from .article import Article
from files.filemanager import FilesManager
import config
import json

fm = FilesManager()

class Crawler(object):

    def __init__(self, number:int = 1):
        '''
        The Crawler will request every url present on the article list file in config send the content into the Articles model for the treatment. It needs as input the number of urls that you want to read
        '''
        self.number = int(number)
        article_list = fm.read(config.path['article_list'])
        self.read_list(article_list)

    def read_list(self, article_list: list):
        '''
        Looping over the article_list file given as argument
        '''
        start_time = time.time()
        articles = []
        i = 0
        while i < self.number: 
            print('In progress: '+str(i+1)+"/"+str(self.number))
            url = article_list.readline()
            i+=1
            try:
                raw = requests.get("http://"+url, allow_redirects=True) #activate for allowing to be reditected to the content
                article = Article(url, raw)
                articles.append(article.asJSON())
            except:
                #in case the crawler is rejected from a website because there is to many requests, we simulate human behaviour with a timer
                time.sleep(1)
                continue
            fm.write(articles, config.path['json_result'],True)
        
        elapsed_time = str(int((time.time() - start_time)*10)/10)    #performance tracking
        print("Processed in " + elapsed_time + " seconds")
        return True
