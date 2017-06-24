from functions import getValue
from functions import function
from http_api import aliyun_api
import json
import numpy

from stock import Stock


appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
code1 = '600215'
code2 = '000001'
ref_List = {'KtimeType': '60',
            'KbeginDay': '20170101',
            'KgetLength': 10,
            'TdayLength': 5,
            'TgetLength': 3,
            'appcode': appcode}

s = Stock(code1, ref_List)
s.get_KValue()
print(s.Kvalue)


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
