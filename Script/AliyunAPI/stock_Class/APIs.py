import os
import pymysql
import urllib.request
import urllib.error
import urllib.parse
import socket
import math
import json
import time
import sys

from file_io import txt, jsonFiles
from functions import getValue, function
from stock_Class.MySQL import MySQL
from multiprocessing.dummy import Pool as ThreadPool

aliyun_appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
showapi_appcode = '6a09e5fe3e724252b35d571a0b715baa'
tempPath = 'z:/test/codeList.txt'
needCodeRefresh = 0


class ResultDeal:
    def __init__(self):
        self._ArrayResult = []
        self._DictResult = {}
        self._title = None

    def setResultArrayAppend(self, tempArg):
        self._ArrayResult.append(tempArg)

    def getArrayResultValue(self):
        return self._ArrayResult

    def resetArrayResultValue(self):
        self._ArrayResult = []

    def setResultDictAppend(self, key, tempArg):
        self._DictResult[key].append(tempArg)

    def getDictResultValue(self):
        return self._DictResult

    def resetDictResultValue(self):
        self._DictResult = {}

    def setTitle(self, title):
        if self._title:
            pass
        else:
            self._title = title

    def getTitle(self):
        return self._title


def multiPool(funcIn, codeListIn, objIn, PoolLength=50):
    # PoolLength = 50
    length = len(codeListIn)
    # r = ResultDeal()
    for i in range(0, length, PoolLength):
        realList = codeListIn[i:i + PoolLength]
        realLength = len(realList)
        function.view_bar(i + realLength, length)
        pool = ThreadPool(realLength)
        objTemp = [{'code': k, 'obj': objIn} for k in realList]
        pool.map(funcIn, objTemp)
        pool.close()
        pool.join()


def maxVol5Days(arg):
    codeIn = arg['code']
    obj = arg['obj']
    resultIn = getValue.get_timeLine5Days_qtimq(codeIn)
    # print(resultIn)
    maxList = list()
    if resultIn:
        try:
            for k in resultIn:
                for key in k:
                    # print(k[key])
                    # print([i['volume'] for i in k])
                    maxList.append(max([i['volume'] for i in k[key]]))
        except TypeError:
            print(codeIn, '\t', resultIn)
        obj.setResultArrayAppend({'code': codeIn, 'maxVol': max(maxList)})
        # print(codeIn, '\t', max(maxList))


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


func = maxVol5Days
r = ResultDeal()
multiPool(func, codeList, r)

print()
for j in r.getArrayResultValue():
    print(j)
