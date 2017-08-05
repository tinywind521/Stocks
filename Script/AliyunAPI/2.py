import time
import os

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

KtimeType = eval(input('Please input K time type (ex.0 = 60, 1 = day): '))
beginDate = input('Please input K begin date (ex.20170101): ')
dateLenth = eval(input('Please input K download lenth (ex.200): '))
getLength = eval(input('Please input K display lenth (ex.61): '))

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
    codeList = ['600519']
    # 000837
    # 601998
    # 300506
    # 002695
else:
    if os.path.exists(tempPath):
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

for code in codeList:
    print(code)
    temp = {'code': '', 'value': 0}
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
    result.append(temp)
    del temp

for i in result:
    if i['result']['001_144BollUpper20BollUpside']['结果'] == 1:
        print(i['code'], end='\t')
        print(i['value'])
        print(i['result'])

"""
1、区分阳线占比的权重
2、上轨以上不超过2次
3、收在上轨以下，中下轨上部空间以上
4、
"""

