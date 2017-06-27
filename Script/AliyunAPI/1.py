from functions import getValue
from functions import function
from http_api import aliyun_api
import json
import numpy
import time

from stock import Stock


appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
code = '000510'
# code2 = '000001'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20170101',
            'KgetLength': 30,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': appcode}
dateList = getValue.get_dateList(ref_List['KbeginDay'], 2 * ref_List['KgetLength'])
ref_List['KbeginDay'] = dateList[0]

# codeList = getValue.get_availableCodeList()
#
# print('start time: ')
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# print('\n')
# codeList = ['600100']
# for code in codeList:
#     print(code)
#     s = Stock(code, ref_List)
#     s.get_KValue()
#     # print(s.Kvalue)
#     s.update_Kstatus()
#     # for k in s.Kvalue:
#     #     print(k)
# print('\nend time:')
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

print(code)
s = Stock(code, ref_List)
s.get_KValue()
# print(s.Kvalue)
s.update_Kstatus()
for k in s.Kvalue:
    print(k)



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
