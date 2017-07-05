import time

from file_io import dict2CSV
from functions import getValue
from stock_Class.stock import Stock, Yline

appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20160505',
            'KgetLength': 41,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': appcode}


codeList = ['600215']


for code in codeList:
    s = Stock(code, ref_List)
    s.get_KValue()
    s.update_Kstatus()
    y = Yline(s.Kvalue, None)
    # for h in y.Index:
    #     print(h)

    print(code)
    print('下面是阳线起点：')
    t = y.get_seq_bull()
    for k in t:
        print(k)

    print('\n下面是阴线起点:')
    for k in y.get_seq_bear():
        print(k)

    print('\n最小量能：')
    print(y.minVol)

