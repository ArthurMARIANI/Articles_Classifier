import json
import config
import os

ROOT_DIR = os.path.abspath(os.curdir)

class FilesManager(object):
    '''
    Allows readingg and writing files located on ./files folder
    '''
    
    def __init__(self):
        open(ROOT_DIR+'/'+config.path['json_result'],
             "w").close()  # clean json result file

    @staticmethod
    def read(filename: str):
        file = open(ROOT_DIR+'/'+filename, 'r')
        return file
        
    @staticmethod
    def write(content:object, filename: str, is_json: bool):
        if (is_json):
            with open(ROOT_DIR+'/'+config.path['json_result'], 'w') as f:
                json.dump(content, f, ensure_ascii=False)
