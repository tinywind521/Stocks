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
                    maxList.append(max([i['volume'] for i in k[key]]))
        except TypeError:
            print(codeIn, '\t', resultIn)
        obj.setResultArrayAppend({'code': codeIn, 'maxVol': max(maxList)})
        # print(codeIn, '\t', maxList)


stocks_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'star2249',
    'db': 'stocks',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

# sDB for stocksDatabase
sDB = MySQL(stocks_config)
sql = 'select gid from dailypreselect;'
sDB.execSQL(sql)
dailyList = [gid['gid'][0:6] for gid in sDB.dbReturn]
# print(dailyList)
# dailyList = ['600569']

func = maxVol5Days
r = ResultDeal()
multiPool(func, dailyList, r)

print()

for j in r.getArrayResultValue():
    # print(j)
    if j['code'][0] == '6':
        code = j['code'] + '.SH'
    elif j['code'][0] == '0' or j['code'][0] == '3':
        code = j['code'] + '.SZ'
    else:
        pass
    sql = "update dailypreselect SET gsharevol='" + format(j['maxVol'] * 100, 'd') + "' where gid='" + code + "';"
    # print(sql)
    sDB.execTXSQL(sql)
