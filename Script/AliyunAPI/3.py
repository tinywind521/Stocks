import os
import sys
import time

from file_io import txt, jsonFiles
from functions import getValue, function
from stock_Class.stock import Stock, Yline, ResultDeal
from stock_Class.MySQL import MySQL
from multiprocessing.dummy import Pool as ThreadPool
from functions import getValue


tempPath = 'z:/test/codeList.txt'

"""前期参数设定"""
KtimeType = 1
beginDate = ''
dateLenth = 160
getLength = 61
debuger = 0
needCodeRefresh = 0

"""获取code列表"""
if debuger:
    codeList = ['601001', '600621']
else:
    if os.path.exists(tempPath):
        if needCodeRefresh == '1':
            print('refreshing...')
            codeList = getValue.get_allCodelist()
            text = ''
            for code in codeList:
                text += code + '\n'
            txt.txt_write(text, tempPath)
        else:
            print('file is exist.')
            f = open(tempPath, 'r')
            text = f.read()
            f.close()
            codeList = text.splitlines()
    else:
        print('file is not exist.')
        codeList = getValue.get_allCodelist()
        text = ''
        for code in codeList:
            text += code + '\n'
        txt.txt_write(text, tempPath)

"""开始计算日线"""

length = len(codeList)


def printTimeLine(codeIn):
    print('\r', codeIn, '\t', getValue.get_timeLine_qtimq(codeIn))

while True:
    PoolLength = 50
    for i in range(0, length, PoolLength):
        realList = codeList[i:i + PoolLength]
        realLength = len(realList)
        pool = ThreadPool(realLength)
        pool.map(printTimeLine, realList)
        pool.close()
        pool.join()
