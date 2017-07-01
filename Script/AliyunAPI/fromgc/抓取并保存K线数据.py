import time

from file_io import dict2CSV
from functions import getValue
from stock_Class.stock import Stock

appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
code = '000510'
# code2 = '000001'
ref_List = {'KtimeType': 'day',
            'KbeginDay': '20160701',
            'KgetLength': 200,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': appcode}
dateList = getValue.get_dateList(ref_List['KbeginDay'], 0)
print(dateList)
# ref_List['KgetLength'] = len(dateList)
ref_List['KbeginDay'] = '20160701'
dateList = getValue.get_dateList(ref_List['KbeginDay'], 0)
ref_List['KbeginDay'] = dateList[0]
print(dateList)
print(ref_List)

codeList = getValue.get_allCodelist()

print('start time: ')
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('\n')
# codeList = ['000007']
header = ['代码', 'min', 'open', 'volumn', 'time', 'max', 'close', 'lastclose', 'mid', 'upper', 'lower',
          '涨幅', '开收', '量能', '上针', '下针', '布林', '轨距', '层级', '趋势', '平台', '预留', '备用']
# header = ['代码', 'min', 'minute', 'open', 'volumn', 'time', 'max', 'close', 'lastclose', 'mid', 'upper', 'lower',
#           '涨幅', '开收', '量能', '上针', '下针', '布林', '轨距', '层级', '趋势', '平台', '预留', '备用']
dict2CSV.writeHeader('Z:\Test\Test.csv', header)

for code in codeList:
    print(code)
    s = Stock(code, ref_List)
    s.get_KValue()
    # print(s.Kvalue)
    s.update_Kstatus()
    # for k in s.Kvalue:
    #     print(k)
    code_text = getValue.add_index()

    Kvalue = []
    try:
        for k in s.Kvalue:
            # print(k)
            temp = {'code': ''}
            temp['code'] = code_text
            temp.update(k)
            Kvalue.append(temp)
        # print(Kvalue)
        dict2CSV.writeRows('Z:\Test\Test.csv', Kvalue)
    except TypeError:
        pass

print('\nend time:')
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


