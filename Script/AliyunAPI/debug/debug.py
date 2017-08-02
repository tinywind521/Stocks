from functions import getValue, function
from stock_Class.stock import Stock, Yline

aliyun_appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
showapi_appcode = '6a09e5fe3e724252b35d571a0b715baa'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20170701',
            'KgetLength': 61,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': aliyun_appcode}
code = '000001'
s = Stock(code, ref_List)
print(s.get_KValue())