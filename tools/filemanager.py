import json
import config
import os


class FilesManager(object):
    '''
    Allows readingg and writing files located on ./files folder
    '''
    
    def __init__(self, dirpath = None):
        self.ROOT_DIR = os.path.abspath(os.curdir)
        if dirpath:
            self.ROOT_DIR += dirpath
        open(self.ROOT_DIR+'/'+config.path['json_result'],
             "w").close()  # clean json result file

    def read(self, filename: str):
        file = open(self.ROOT_DIR+'/'+filename, 'r')
        return file
        
    def write(self, content:object, filename: str, is_json: bool):
        if (is_json):
            with open(self.ROOT_DIR+'/'+config.path['json_result'], 'w') as f:
                json.dump(content, f, ensure_ascii=False)
