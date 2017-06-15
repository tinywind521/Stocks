import time
import json
import numpy

from functions import function
from aliyun import aliyun_api
from aliyun import QQ_api


def get_dateList(beginDay, getLength, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    截取指定长度的日起序列
    :param beginDay:
    :param getLength: 所需日期长度
    :param appcode:
    :return:
    """
    # beginDay = input('Enter beginDay: ')
    # getLength = int(input("Enter day's length: "))
    # appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
    dateList = function.return_date(beginDay, appcode)
    # print(dateList)
    if getLength < len(dateList):
        dateList = dateList[-getLength:]
    # print(dateList)
    return dateList


def get_allCodelist(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取当日总表
    :param appcode:
    :return:
    """
    allCodedict = function.return_stocklist(appcode)
    allCodelist = []
    for Codedict in allCodedict:
        allCodelist.append(Codedict['code'])
    return allCodelist


def get_availableCodeList(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取当日需要判断的代码列表
    :param:
    :return:
    """
    ssdlist = get_allssdcode(appcode)
    delList = []
    delList.extend(ssdlist['newStockNetPublishList'])
    delList.extend(ssdlist['stockholderList'])
    delList.extend(ssdlist['stopList'])
    delList.extend(ssdlist['addNewStockNetPublishList'])
    delList.extend(ssdlist['recoverList'])
    delList.extend(ssdlist['shareRegistList'])
    delList.extend(ssdlist['ShareDividendList'])
    delList.extend(ssdlist['stockAlarmList'])
    delList.extend(ssdlist['startList'])

    allCodelist = get_allCodelist(appcode)
    result = [k for k in allCodelist]

    for delCode in delList:
        # print(delCode)
        try:
            result.remove(delCode)
        except ValueError:
            pass
    return result


def get_DateTime():
    """
    获取当前日期和时间
    :return:
    """
    timeStamp = time.localtime()
    # DateTime = {}
    fulldate = (time.strftime("%Y-%m-%d", timeStamp))
    shortdate = (time.strftime("%Y%m%d", timeStamp))
    fulltime = (time.strftime("%H:%M:%S", timeStamp))
    shorttime = (time.strftime("%H%M%S", timeStamp))
    keys = ['fulldate', 'shortdate', 'fulltime', 'shorttime']
    # print(keys)
    values = [fulldate, shortdate, fulltime, shorttime]
    # print(values)
    DateTime = dict(zip(keys, values))

    return DateTime


def get_dataList(aliyun_input):
    """
    解析aliyun返回值的dataList
    :param aliyun_input:
    :return:
    """
    dataList = aliyun_input['showapi_res_body']['dataList']
    return dataList


def get_allssdcode(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取各种非常规的代码，只有代码
    :return:
    newStockNetPublishList          :  首发新股网上发行列表
    stockholderList                 :  股东大会召开列表
    stopList                        :  停牌股票列表
    addNewStockNetPublishList       :  增发新股列表
    recoverList                     :  复牌股票列表
    shareRegistList                 :  分红转增股权登记列表
    ShareDividendList               :  除权除息列表
    stockAlarmList                  :  退市风险警示列表
    startList                       :  上市股票列表
    """
    allssd = function.return_ssd(appcode)
    allkeys = list(allssd)
    key = ''
    allssdcode = {}
    for key in allkeys:
        tempArray = []
        if key.lower().endswith('list'):
            for ssd_element in allssd[key]:
                tempArray.append(ssd_element['code'])
            allssdcode[key] = tempArray

    return allssdcode


def get_CodeLHB(code):
    """
    获取指定代码的LHB信息
    :param code:
    :return:
    """
    lhb_list = QQ_api.lhb_code_list(code)
    i = 0
    result = []
    for f in lhb_list:
        i += 1
        detail = QQ_api.lhb_code_detail(f['code'], f['date'], str(i), f['typeid'])
        for element in detail:
            result.append(element)
    return result


def get_60F(code, beginDay, getLength, n=20, p=2, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取指定日期长度的60F,
    同时计算boll
    :param p: p常量
    :param n: 布林计算天数
    :param code:
    :param beginDay:
    :param getLength: = 2n / 4
    :param appcode:
    :return:
    """
    try:
        dateList = get_dateList(beginDay, getLength)
        aliyun_str = aliyun_api.realtime(code, dateList[0], '60', 'bfq', appcode)
        aliyun_dict = json.loads(aliyun_str)
        dataList = get_dataList(aliyun_dict)
        dataList.reverse()
        realtimeValue = []
        tempVol = 0
        tempOpen = ''
        for element in dataList:
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
        realtimeList = realtimeValue
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
            # print(element['close'])
        # closeList.reverse()
        boll = function.cal_boll(closeList, n, p)
        m = len(boll)
        realtimeList = realtimeList[-m:]
        # tempList = []
        for i in range(0, m):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            realtimeList[i].update(boll[i])
            # print(realtimeList[i])
        # print(realtimeList)
        return realtimeList
    except ValueError:
        return None
