import json
import time

import requests

from tools.monitor import Monitor

class Crawler(object):

    def __init__(self, monitor: Monitor):
        self.monitor = monitor

    def crawl(self, url: str, debug: bool = False):
        req = self.getArticle(url)
        if(hasattr(req, "status_code")):
            status = req.status_code
            self.monitor.appendStatus(code=status)
            if status is 200:
                return req 
            else:
                return status
        else:
            self.monitor.appendStatus(code=404)
            return None
    
    def getArticle(self, url:str) -> object:

        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'CHROME_WIN_UA',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }

        try:
            req = requests.get(
                url="http://"+url, 
                allow_redirects=True,
                headers=headers
            )
            return req

        except:
            return None
        
