'''
This is the main file, the one we are calling and which is launching the crawler
'''
from models.crawler import Crawler
import sys
import config

def main():
    if(config.mode == "test"):
        try :
            number = int(float(sys.argv[1]))*2/2
        except:
            raise Exception("Please give a number as argument or change mode in config file")
            return None
    if(config.mode == "full"):
        number = 100000
    try:
        Crawler(number)  
    except:
        raise Exception(
            "Change mode in config file to test or full value")
        return None
main() #launch the file
