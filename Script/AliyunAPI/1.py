from functions import getValue
from aliyun import aliyun_api
import json
import numpy


def get_60F(code, beginDay, getLength, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取指定日期长度的60F,
    同时计算boll
    :param code:
    :param beginDay:
    :param getLength:
    :param appcode:
    :return:
    """
    try:
        dateList = getValue.get_dateList(beginDay, getLength)
        # print(dateList)
        aliyun_str = aliyun_api.realtime(code, dateList[0], '60', 'bfq', appcode)
        aliyun_dict = json.loads(aliyun_str)
        # print(aliyun_str)

        dataList = getValue.get_dataList(aliyun_dict)
        dataList.reverse()
        realtimeValue = []
        tempVol = 0
        tempOpen = ''
        for element in dataList:
            # print(element)
            # print(element['minute'][-4:])
            if element['minute'][-4:] == '0930':
                tempVol = int(element['volumn'])
                tempOpen = element['open']
            elif element['minute'][-4:] == '1030':
                realVol = format((int(element['volumn']) + tempVol), 'd')
                realOpen = tempOpen
                element['volumn'] = realVol
                element['open'] = realOpen
                realtimeValue.append(element)
            else:
                realtimeValue.append(element)
        return realtimeValue
    except ValueError:
        return None

narray = numpy.array(nlist)
narray = numpy.array
sum1=narray.sum()
narray2=narray*narray
sum2=narray2.sum()
mean=sum1/N
var=sum2/N-mean**2


# 根据日期列表，按照日期，重新计算60F，因为集合竞价问题
# 前阴连阴，连阴后必须连阳，再阴；双阴必须前低后高
# 中间的连阳可以假阳
# 前后都是连阴形态，也要考虑
# 中轨怎么考虑



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