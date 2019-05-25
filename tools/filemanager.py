import json
import config

class FilesManager(object):
    '''
    Allows readingg and writing files located on ./files folder
    '''
    
    def __init__(self):
        open(config.path['json_result'], "w").close() #clean json result file

    @staticmethod
    def read(filename: str):
        file = open(filename, 'r')
        return file
        
    @staticmethod
    def write(content:object, filename: str, is_json: bool):
        if (is_json):
            with open(config.path['json_result'], 'w') as f:
                json.dump(content, f, ensure_ascii=False)