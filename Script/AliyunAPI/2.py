import time

from file_io import dict2CSV
from functions import getValue
from stock_Class.stock import Stock, Yline

appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20160505',
            'KgetLength': 61,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': appcode}


codeList = ['000837']
# 000837
# 601998
# 300506
# 002695
# codeList = getValue.get_allCodelist()

result = []
temp = {'code': '', 'value': 0}

for code in codeList:
    s = Stock(code, ref_List)
    s.get_KValue()
    # for i in s.Kvalue:
    #     print(i)
    s.update_Kstatus()
    # print(s.Kvalue[0:-12])
    y = Yline(s.Kvalue, None)
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
    temp['code'] = code
    temp['value'] = y.status
    print(temp)
    result.append(temp)


