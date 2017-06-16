from functions import getValue
from functions import function
from aliyun import aliyun_api
import json
import numpy

appcode = 'c7689f18e1484e9faec07122cc0b5f9e'

# s = function.return_stocklist(appcode)

c = getValue.get_blockList(appcode)
# print(c)

for ele in c:
    code = ele['code']
    print(code)
    s = function.return_block_stocks(code, appcode)
    print(s)
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


