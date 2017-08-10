import time
import os
import json

from file_io import txt
from functions import getValue
from stock_Class.stock import Stock, Yline

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

KtimeType = 1
beginDate = ''
dateLenth = 160
getLength = 61
needRefresh = input('Want to refresh codeList? (1/0): ')

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
        if needRefresh == '1':
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


result = []
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
    # t = y.get_list_bull()
    # for k in t:
    #     print(k)

    # print('\n下面是阴线起点:')
    # for k in y._list_bull():
    #     m = [(l['time'], l['序号']) for l in k]
    #     print(m)

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
    y.cal_patternResult()
    temp['code'] = code
    temp['value'] = y.status
    temp['result'] = y.patternResult
    # print(temp)
    if temp['result']['001_144BollUpper20BollUpside']['结果'] == 1:
        result.append(temp)
    del temp

codeList = [k['code'] for k in result]

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

for code in codeList:
    print(code)
    temp = {'code': code, 'value': 0, 'result': {'001_144BollUpper20BollUpside': {}, }}
    # s = Stock(code, ref_List)
    # s.get_KValue()
    # s.update_Kstatus()
    # try:
    #     y = Yline(s.Kvalue, None)
    # except ValueError:
    #     continue
    # temp['code'] = code
    # temp['value'] = y.status
    result60.append(temp)
    del temp

finalResult = {}
tempNum = 0
print('代码,总层级得分,近期层级类型,最近一次层级差得分,回调次数,位于20布林,位于144布林,近期最大涨幅,')
for i in result:
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
with open(outputRootPath + '/strategy.json', 'w+') as f:
    json.dump(finalResult, f)

allBlockCode = getValue.get_blockList_showapi()
allBlockList = []
for BlockList in allBlockCode:
    BlockListReturn = getValue.get_blockStocks_showapi(BlockList['code'])
    if BlockListReturn:
        allBlockList.append(BlockListReturn)

BlockResultHY = {'codeList': [], }.clear()
BlockResultGN = {'codeList': [], }.clear()

for i in result60:
    code = i['code']
    for BlockList in allBlockList:
        if code in BlockList['block_stocksList']:
            if BlockList['name'].find('证监会行业') != -1:
                print(BlockList)
                if BlockResultHY is None:
                    BlockResultHY = dict.fromkeys([BlockList['name']])
                    BlockResultHY[BlockList['name']] = [code]
                elif BlockList['name'] in BlockResultHY:
                    # BlockResultHY[BlockList['name']] += 1
                    BlockResultHY[BlockList['name']].append(code)
                else:
                    # BlockResultHY[BlockList['name']] = 1
                    BlockResultHY[BlockList['name']] = [code]
            elif BlockList['name'].find('概念板块') != -1:
                if BlockResultGN is None:
                    BlockResultGN = dict.fromkeys([BlockList['name']])
                    BlockResultGN[BlockList['name']] = [code]
                elif BlockList['name'] in BlockResultGN:
                    # BlockResultGN[BlockList['name']] += 1
                    BlockResultGN[BlockList['name']].append(code)
                else:
                    # BlockResultGN[BlockList['name']] = 1
                    BlockResultGN[BlockList['name']] = [code]
            else:
                pass

hyList = list(BlockResultHY.keys())
# print(hyList)
gnList = list(BlockResultGN.keys())
# print(gnList)
allList = list(hyList + gnList)
BlockResultKeys = sorted(allList)

# 写入 JSON 数据
with open(outputRootPath + '/001/BlockResultHY.json', 'w+') as f:
    json.dump(BlockResultHY, f)
with open(outputRootPath + '/001/BlockResultGN.json', 'w+') as f:
    json.dump(BlockResultGN, f)

BlockResult = BlockResultHY
BlockResult.update(BlockResultGN)
for key in BlockResultKeys:
    print(key, ',', BlockResult[key])

"""
1、/001文件夹和文件的存在性；
2、板块代码每周刷新一次；
3、261同学的相对路径问题；
4、文件整合；
5、添加名称显示

"""

print('代码,60F层级得分')
for i in result60:
    print(i['code'], end=',')
    print(format(i['value'], '.3f'), end=',')
    print('')

