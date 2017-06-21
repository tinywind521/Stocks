from functions import getValue
from functions import function
from http_api import aliyun_api
import json
import numpy

from stock import Stock


appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
code1 = '002839'
code2 = '000001'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20170101',
            'KgetLength': 10,
            'TdayLength': 1,
            'TdataLength': 242,
            'appcode': appcode}

s = Stock(code1, ref_List)
# s2 = Stock(code2, ref_List)

s.get_KValue()
print(s.Kvalue)
print(s.get_KtimeType())

s.set_KtimeType('day')
s.set_Refresh()

print(s.Kvalue)
s.get_KValue()
print(s.get_KtimeType())

# for k in s1.value:
#     print(k)

print(s.boll_mid())
print(s.boll_upper())
print(s.boll_lower())

# s = function.return_stocklist(appcode)

# c = getValue.get_blockList(appcode)
# print(c)
#
# for ele in c:
#     code = ele['code']
#     print(code)
#     s = function.return_block_stocks(code, appcode)
#     print(s)
# s = function.return_block_stocks('hangye_ZB49', appcode)
# print(s)



# def ss(string=[]):
#     for s in string:
#         print(s)
#     return None
# try:
#     d = input('Input Reference: ')
#     dd = list(d)
#     print(dd)
#     ss(dd)
# except:
#     print('Ref Error!')



# 多级路径引入函数

# import sys
# import os
# sys.path.append(os.getcwd()+'\\parent\\child')
#
# print(sys.path)
#
# from a import add_func
#
#
# print (sys.path)
#
# print ("Import add_func from module a")
# print ("Result of 1 plus 2 is: ")
# print (add_func(1,2))
