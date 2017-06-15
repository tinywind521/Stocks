from functions import getValue
from functions import function
from aliyun import aliyun_api
import json
import numpy


codeList = getValue.get_availableCodeList()
dateList = getValue.get_dateList('20170101', 10)
i = 0
for code in codeList:
    i += 1
    s = getValue.get_60F(code, dateList[0], 10)
    print(format(i, '04d') + '\t' + code + '\t' + format(len(s), 'd'))



# 前阴连阴，连阴后必须连阳，再阴；双阴必须前低后高
# 中间的连阳可以假阳
# 前后都是连阴形态，也要考虑
# 中轨怎么考虑
# 找第一组连阴 和 第二组连阴（真阴） 以及中间的阳线



# print(c)

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



# 多级路径函数

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


