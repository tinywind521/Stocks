import sys
import os
import pymysql
import time

from file_io import txt, jsonFiles
from functions import getValue, function
from stock_Class.stock import Stock, Yline
from stock_Class.MySQL import MySQL
from multiprocessing.dummy import Pool as ThreadPool


def view_bar(num, total, codeIn):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    r = '\r[%s%s] %2.2f%% %d/%d %s' % ("|"*flow, " "*(100-flow), rate_num, num, total, codeIn,)
    sys.stdout.write(r)
    sys.stdout.flush()


class Result:
    def __init__(self, firstValue):
        self._result = firstValue

    def resultAppend(self, key, tempArg):
        self._result[key].append(tempArg)

    def getResultValue(self):
        return self._result


def calDayStatus(obj):
    codeArg = obj['codeArg']
    objResult = obj['objResult']
    ref_List = obj['ref_List']
    tempArg = {'code': '', 'value': 0, 'result': {'001_144BollUpper20BollUpside': {}}}
    s = Stock(codeArg, ref_List)
    while True:
        try:
            s.get_KValue()
            s.update_Kstatus()
            len(s.Kvalue)
            break
        except (TypeError, IndexError):
            time.sleep(5)
    if len(s.Kvalue) >= 5:
        try:
            y = Yline(s.Kvalue, None)
        except ValueError:
            return
        y.cal_patternResult(ref_List['KtimeType'])
        tempArg['code'] = codeArg
        tempArg['value'] = round(y.status, 3)
        tempArg['result'] = y.patternResult
        print(codeArg)
        if tempArg['result']['001_144BollUpper20BollUpside']['结果'] == 1:
            objResult.resultAppend('001', tempArg)
        if tempArg['result']['101_20BollDay4B']['结果'] == 1:
            objResult.resultAppend('101', tempArg)
        del tempArg
    else:
        pass


aliyun_appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
showapi_appcode = '6a09e5fe3e724252b35d571a0b715baa'
tempPath = 'z:/test/codeList.txt'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20170701',
            'KallLength': 160,
            'KgetLength': 61,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': aliyun_appcode}

"""前期参数设定"""
KtimeType = 1
beginDate = ''
dateLenth = 160
getLength = 61
debuger = input('Want to debuger? (1/0): ')
needCodeRefresh = input('Want to refresh codeList? (1/0): ')
needBlockRefresh = input('Want to refresh blockList? (1/0): ')
needNameRefresh = input('Want to refresh nameList? (1/0): ')

ref_List['KallLength'] = dateLenth

if KtimeType == 1:
    ref_List['KtimeType'] = 'day'
else:
    ref_List['KtimeType'] = '60'

if getLength:
    ref_List['KgetLength'] = getLength
else:
    ref_List['KgetLength'] = 61

"""获取code列表"""
if debuger:
    codeList = ['002603', '002460']
    # 000837
    # 601998
    # 300506
    # 002695
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
result = {
    '001': [],
    '101': [],
}

temp = {'code': '', 'value': 0, 'result': {}}
NameList = {}

length = len(codeList)
PoolLength = 20
# Make the Pool of workers
r = Result(result)
for i in range(0, len(codeList), PoolLength):
    realList = codeList[i:i + PoolLength]
    realLenth = len(realList)
    pool = ThreadPool(realLenth)
    objTemp = [{'codeArg': k, 'objResult': r, 'ref_List': ref_List} for k in realList]
    results = pool.map(calDayStatus, objTemp)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()


