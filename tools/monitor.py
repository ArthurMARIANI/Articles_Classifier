from terminaltables import AsciiTable
import os
import numpy as np
import time
from tools.utils import Utils

class Monitor(object):
    '''
    Contains attributes and fonction related to articles 
    [url, website, title, content, author]
    '''
    utils = Utils()

    def __init__(self):
        self.to_print = []
        self.words_list = []
        self.dic = {}
        self.status = {
            "total": 0,
            "success": 0,
            "errors": {
                403:0,
                404:0,
                503:0,
            }
        }

    def appendAdvance(self, advance:int, total:int, time:int):
        data = []
        estimated = round((time/advance)*(total-advance),1)
        data.append([advance, total, time, estimated])
        self.buildTable("Advance", ["advance", "total", "time", "left"], data)

    def appendWords(self, words: int):
        data = []
        if words:
            self.words_list.append(words)
        if self.words_list:
            percentiles_list = [0, 20, 40, 60, 80, 100]
            percentiles = np.percentile(self.words_list, percentiles_list)
            i = 0
            for percentile in percentiles:
                data.append([percentiles_list[i], int(percentile)])
                i += 1
            self.buildTable("Words", ["Percentile", "Number"], data)

    def appendStatus(self, code:int):
        data = []
        self.status['total'] += 1
        if code == 200:
            self.status["success"] +=1
        else:
            self.status["errors"][code] += 1
        data.append(["200 (success)", self.status["success"], int(
            self.status["success"]/self.status['total']*100)])

        for error in self.status["errors"]:
            data.append([error, self.status['errors'][error],int(self.status['errors'][error]/self.status['total']*100)])

        self.buildTable(
            "Status", ['Load_Status', 'Number', 'Proportion'], data)

    def buildTable(self, title:str = None, headers:str = None , content:str = None):
        table_data = [headers]
        for element in content:
            table_data.append(element)
        table = AsciiTable(table_data) 
        self.to_print.append('\n'+'+ '+title.upper())
        self.to_print.append(table.table)
        
    def clearMonitor(self):
        self.to_print = []

    def updatePrint(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for e in self.to_print:
            print(e)
        
        
