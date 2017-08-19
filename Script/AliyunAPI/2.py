import time
import os
import json
import pymysql

from file_io import txt, jsonFiles
from functions import getValue
from stock_Class.stock import Stock, Yline
from stock_Class.MySQL import MySQL

aliyun_appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
showapi_appcode = '6a09e5fe3e724252b35d571a0b715baa'
tempPath = 'z:/test/codeList.txt'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20170701',
            'KgetLength': 61,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': aliyun_appcode}

# KtimeType = eval(input('Please input K time type (ex.0 = 60, 1 = day): '))
# beginDate = input('Please input K begin date (ex.20170101): ')
# dateLenth = eval(input('Please input K download lenth (ex.200): '))
# getLength = eval(input('Please input K display lenth (ex.61): '))
"""前期参数设定"""
KtimeType = 1
beginDate = ''
dateLenth = 160
getLength = 61
needCodeRefresh = input('Want to refresh codeList? (1/0): ')
needBlockRefresh = input('Want to refresh blockList? (1/0): ')
needNameRefresh = input('Want to refresh nameList? (1/0): ')

if KtimeType == 1:
    ref_List['KtimeType'] = 'day'
else:
    ref_List['KtimeType'] = '60'

if getLength:
    ref_List['KgetLength'] = getLength
else:
    ref_List['KgetLength'] = 61

if len(beginDate) == 8:
    ref_List['KbeginDay'] = beginDate
elif not beginDate:
    if ref_List['KtimeType'] == '60':
        dateList = getValue.get_dateList('20170101', 50)
        ref_List['KbeginDay'] = dateList[-int(dateLenth / 4) - 1]
    elif ref_List['KtimeType'] == 'day':
        dateList = getValue.get_dateList('20150101', 400)
        ref_List['KbeginDay'] = dateList[-int(dateLenth) - 1]
    else:
        ref_List['KbeginDay'] = '20170101'
else:
    pass

"""获取code列表"""
# print(ref_List)
debuger = 0

if debuger:
    codeList = ['600362', '002460']
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
# print(codeList)
NameList = {}

for code in codeList:
    print(code)
    temp = {'code': '', 'value': 0, 'result': {'001_144BollUpper20BollUpside': {}}}
    s = Stock(code, ref_List)
    s.get_KValue()
    # print(s.Kvalue)
    # for i in s.Kvalue:
    #     print(i)
    s.update_Kstatus()
    # for i in s.Kvalue:
    #     print(i)
    # print(s.Kvalue)
    # print(s.Kvalue[0:-12])
    # print(s.Kvalue)
    try:
        y = Yline(s.Kvalue, None)
    except ValueError:
        continue
    # m = [(l['time'], l['序号'], l['布林'], l['量能']) for l in y.Index]
    # for h in m:
    #     print(h)

    # print(code)
    # print('下面是阳线起点：')
    # t = y.get_seq_bull()
    # for k in t:
    #     print(k)
    #
    # print('\n下面是阴线起点:')
    # for k in y.get_seq_bear():
    #     m = [(l['time'], l['序号']) for l in k]
    #     print(m)
    #
    # print('\n下面是全部K线:')
    # for k in y.get_seq_all():
    #     m = [(l['time'], l['序号'], l['底部']) for l in k]
    #     print(m)

    # print('\n阴线分段分层：')
    # for k in y.get_levelList():
    #     m = [(l['time'], l['序号']) for l in k]
    #     print(m)

    # print('\n最小量能：')
    # print(y.minVol)
    y.cal_patternResult(ref_List['KtimeType'])
    temp['code'] = code
    temp['value'] = y.status
    temp['result'] = y.patternResult
    # print(temp)
    if temp['result']['001_144BollUpper20BollUpside']['结果'] == 1:
        result['001'].append(temp)
    if temp['result']['101_20BollDay4B']['结果'] == 1:
        result['101'].append(temp)
    del temp
    # print(y.get_all_length())
    # print(y.get_bear_length())
    # print(y.get_bull_length())
    # print(y.levelTimes)
    # for m in y.patternResult:
    #     for n in y.patternResult[m]:
    #         print(n, end=': ')
    #         print(y.patternResult[m][n])

# print(result['101'])
codeList = [k['code'] for k in result['101']]
# print(codeList)

ref_List = {'KtimeType': '60',
            'KbeginDay': '',
            'KgetLength': 61,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': aliyun_appcode}

if len(beginDate) == 8:
    ref_List['KbeginDay'] = beginDate
elif not beginDate:
    if ref_List['KtimeType'] == '60':
        dateList = getValue.get_dateList('20170101', 50)
        ref_List['KbeginDay'] = dateList[-int(dateLenth / 4) - 1]
    elif ref_List['KtimeType'] == 'day':
        dateList = getValue.get_dateList('20150101', 400)
        ref_List['KbeginDay'] = dateList[-int(dateLenth) - 1]
    else:
        ref_List['KbeginDay'] = '20170101'
else:
    pass

result60 = []
temp = {'code': '', 'value': 0, 'result': {}}
# print(codeList)
# print(ref_List)

for code in codeList:
    print(code)
    temp = {'code': code, 'value': 0, 'result': {'001_144BollUpper20BollUpside': {}, }}
    s = Stock(code, ref_List)
    s.get_KValue()
    # print(s.Kvalue)
    s.update_Kstatus()
    try:
        y = Yline(s.Kvalue, None)
    except ValueError:
        continue
    y.cal_patternResult(ref_List['KtimeType'])
    temp['code'] = code
    temp['value'] = y.status
    temp['result'] = y.patternResult
    result60.append(temp)
    del temp
    for m in y.patternResult:
        for n in y.patternResult[m]:
            print(n, end=': ')
            print(y.patternResult[m][n])

finalResult = {}
tempNum = 0
print('代码,总层级得分,近期层级类型,最近一次层级差得分,回调次数,位于20布林,位于144布林,近期最大涨幅,')
for i in result['001']:
    print(i['code'], end=',')
    print(format(i['value'], '.3f'), end=',')
    print(i['result']['001_144BollUpper20BollUpside']['近期层级类型'], end=',')
    print(format(i['result']['001_144BollUpper20BollUpside']['层级差得分'], '.3f'), end=',')
    print(i['result']['001_144BollUpper20BollUpside']['回调次数'], end=',')
    print(i['result']['001_144BollUpper20BollUpside']['K线位于20布林位置'], end=',')
    print(i['result']['001_144BollUpper20BollUpside']['K线位于144布林位置'], end=',')
    print(i['result']['001_144BollUpper20BollUpside']['近期最大涨幅'], end=',')
    print('')
    for j in list(i['result'].keys()):
        if i['result'][j]['名称'] in finalResult.keys():
            # finalResult[i['result'][j]['名称']].append(i['code'])
            pass
        else:
            tempNum += 1
            finalResult[i['result'][j]['名称']] = format(tempNum, '03d')


# 写入 JSON 数据
outputRootPath = 'Z:/Test'

path = outputRootPath + '/strategy.json'
jsonFiles.Write(path, finalResult)

# allBlockList
path = outputRootPath + '/allBlockList.json'
if needBlockRefresh == '1' or not os.path.exists(path):
    print('Refreshing blockList...')
    allBlockCode = getValue.get_blockList_showapi()
    allBlockList = []
    for BlockList in allBlockCode:
        BlockListReturn = getValue.get_blockStocks_showapi(BlockList['code'])
        if BlockListReturn:
            allBlockList.append(BlockListReturn)
    # 写入 JSON 数据
    jsonFiles.Write(path, allBlockList)
else:
    pass

# allNameList
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
sql = 'select gid, name from pandc'
sDB.execSQL(sql)
nameList = {}
for i in sDB.dbReturn:
    nameList[i['gid'].split('.')[0]] = i['name']

path = outputRootPath + '/allNameList.json'
if needNameRefresh == '1' or not os.path.exists(path):
    # 写入 JSON 数据
    jsonFiles.Write(path, nameList)
else:
    pass

path = outputRootPath + '/allBlockList.json'
allBlockList = jsonFiles.Read(path)

BlockResultHY = {'codeList': [], }.clear()
BlockResultGN = {'codeList': [], }.clear()

for i in result60:
    code = i['code']
    for BlockList in allBlockList:
        if code in BlockList['block_stocksList']:
            if BlockList['name'].find('证监会行业') != -1:
                # print(BlockList)
                if BlockResultHY is None:
                    BlockResultHY = dict.fromkeys([BlockList['name']])
                    BlockResultHY[BlockList['name']] = [code]
                elif BlockList['name'] in BlockResultHY:
                    BlockResultHY[BlockList['name']].append(code)
                else:
                    BlockResultHY[BlockList['name']] = [code]
            elif BlockList['name'].find('概念板块') != -1:
                if BlockResultGN is None:
                    BlockResultGN = dict.fromkeys([BlockList['name']])
                    BlockResultGN[BlockList['name']] = [code]
                elif BlockList['name'] in BlockResultGN:
                    BlockResultGN[BlockList['name']].append(code)
                else:
                    BlockResultGN[BlockList['name']] = [code]
            else:
                pass
try:
    hyList = list(BlockResultHY.keys())
    # print(hyList)
    gnList = list(BlockResultGN.keys())
    # print(gnList)
    allList = list(hyList + gnList)
    BlockResultKeys = sorted(allList)

    # 写入 JSON 数据

    path = outputRootPath + '/001/BlockResultHY.json'
    jsonFiles.Write(path, BlockResultHY)

    path = outputRootPath + '/001/BlockResultGN.json'
    jsonFiles.Write(path, BlockResultGN)

    BlockResult = BlockResultHY
    BlockResult.update(BlockResultGN)
    for key in BlockResultKeys:
        print(key, ',', BlockResult[key])
except AttributeError:
    pass


"""
1、/001文件夹和文件的存在性；
3、261同学的相对路径问题；

1、20 B3（上半空间下部） 、144 >=3 首次 开始统计下降层级差 V U次数 <=2

"""

print('代码,60F层级得分')
for i in result60:
    print(i['code'], end=',')
    print(format(i['value'], '.3f'), end=',')
    print('')

