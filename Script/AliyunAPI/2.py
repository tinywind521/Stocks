import os
import pymysql
import time
from file_io import txt, jsonFiles
from functions import getValue, function
from stock_Class.stock import Stock, Yline
from stock_Class.MySQL import MySQL

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

i = 0
length = len(codeList)
for code in codeList:
    # print(code)
    i += 1
    function.view_bar(i, length, code)
    temp = {'code': '', 'value': 0, 'result': {'001_144BollUpper20BollUpside': {}}}
    s = Stock(code, ref_List)
    while True:
        try:
            s.get_KValue()
            s.update_Kstatus()
            len(s.Kvalue)
            break
        except TypeError:
            time.sleep(5)
    if len(s.Kvalue) >= 5:
        try:
            y = Yline(s.Kvalue, None)
        except ValueError:
            continue
        y.cal_patternResult(ref_List['KtimeType'])
        temp['code'] = code
        temp['value'] = round(y.status, 3)
        temp['result'] = y.patternResult
        # print(temp)
        if temp['result']['001_144BollUpper20BollUpside']['结果'] == 1:
            result['001'].append(temp)
        if temp['result']['101_20BollDay4B']['结果'] == 1:
            result['101'].append(temp)
        del temp
    else:
        pass
print()

ref_List = {'KtimeType': '60',
            'KbeginDay': '',
            'KallLength': 160,
            'KgetLength': 61,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': aliyun_appcode}
ref_List = getValue.get_beginDate(ref_List, dateLenth, beginDate)

result60 = {
                '001': [],
                '101': [],
            }
temp = {'code': '', 'valueDay': 0, 'value60F': 0, 'result': {}}

i = 0
length = len(result['101'])
for element in result['101']:
    # print(element['code'])
    i += 1
    function.view_bar(i, length, code)
    temp = {'code': '', 'valueDay': 0, 'value60F': 0, 'result': {'101_20Boll60F4B': {}}}
    s = Stock(element['code'], ref_List)
    while True:
        try:
            s.get_KValue()
            s.update_Kstatus()
            len(s.Kvalue)
            break
        except TypeError:
            time.sleep(5)
    if len(s.Kvalue) >= 5:
        try:
            y = Yline(s.Kvalue, None)
        except ValueError:
            continue
        y.cal_patternResult(ref_List['KtimeType'])
        temp['code'] = element['code']
        temp['valueDay'] = element['value']
        temp['value60F'] = round(y.status, 3)
        # print(element['result'])
        # print({'101_20Boll60F4B': y.patternResult['101_20Boll60F4B']})
        if y.patternResult:
            tempdict = element['result']
            tempdict.update({'101_20Boll60F4B': y.patternResult['101_20Boll60F4B']})
            temp['result'] = tempdict
        else:
            temp['result']['101_20Boll60F4B']['结果'] = 0
        if temp['result']['101_20Boll60F4B']['结果'] == 1:
            if (2 > temp['result']['101_20BollDay4B']['K线位于20布林位置'] >= 1 or
                2 > temp['result']['101_20Boll60F4B']['K线位于20布林位置'] >= 1) and \
                    (temp['result']['101_20BollDay4B']['中轨状态'] >= 0 or temp['result']['101_20Boll60F4B']['中轨状态'] >= 0):
                """
                布林斜率？
                必须叠加倍量
                回调次数等于1的时候接收下降.
                
                （60F如果是下降层级）往15F找，同时对15F的层级差进行一次判断主要是最近层级差 不是下降！再结合倍量
                阳线占比与层级差
                
                反转瓶颈
                
                """
                if temp['result']['101_20Boll60F4B']['阳线占比'] >= 75:
                    result60['101'].append(temp)
                elif temp['result']['101_20Boll60F4B']['阳线占比'] >= 25 and temp['result']['101_20Boll60F4B']['层级差得分'] >= 80:
                    result60['101'].append(temp)
                else:
                    pass
        del temp
    else:
        pass

print('\n')
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

print('\n')

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

for i in result['001']:
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
    # for key in BlockResultKeys:
    #     print(key, ',', BlockResult[key])
except AttributeError:
    pass

# print('代码,60F层级得分')
print('\n')
print('形态101：')
for i in result60['101']:
    print(i['code'])
    if i['code'][0] == '6':
        code = i['code'] + '.SH'
    elif i['code'][0] == '0' or i['code'][0] == '3':
        code = i['code'] + '.SZ'
    else:
        pass
    sql = "replace dailypreselect SET gid='" + code + "';"
    sDB.execTXSQL(sql)
