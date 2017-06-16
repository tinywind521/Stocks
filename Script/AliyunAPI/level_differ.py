from functions import getValue
from functions import function
from aliyun import aliyun_api
import json
import numpy


# codeList = getValue.get_availableCodeList()
# dateList = getValue.get_dateList('20170101', 10)
# print(dateList[0])
n = 20
i = 0
# for code in codeList:

i += 1
# s = getValue.get_60F(code, dateList[0], 10, n)
s = getValue.get_60F('000762', '20170605', 10, n)
# print(s)
# op = 0
# close = 0
# lastclose = 0
# vol = 0
k_list = []
if len(s) == n:
    for element in s:
        element['open'] = float(element['open'])
        element['close'] = float(element['close'])
        element['volumn'] = int(element['volumn'])
        # print(element)
        k_list.append(element)
    k_list.reverse()
    flag = False
    if k_list[0]['mid'] + 0.01 >= k_list[1]['mid']:
        "判断 mid 已平"
        "N : Negative"
        "P : Passive"
        first_N = []
        second_N = []
        for i in range(0, 8):
            k_value = k_list[0]
            if i >= 4 and not flag:
                break
            if (k_value['close'] - k_value['lastclose']) <= 0 and (k_value['close'] - k_value['open']) <= 0:
                first_N.append(k_value)
                flag = True
            else:
                if flag:
                    break
            k_list.pop(0)
        print(k_list)
        print(first_N)
        flag = False
        for i in range(0, 8):
            k_value = k_list[0]
            if i >= 4 and not flag:
                break
            if (k_value['close'] - k_value['lastclose']) <= 0 and (k_value['close'] - k_value['open']) <= 0:
                second_N.append(k_value)
                flag = True
            else:
                if flag:
                    break
            k_list.pop(0)
        print(k_list)
        print(second_N)

# print(format(i, '04d') + '\t' + code + '\t' + format(len(s), 'd'))



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


