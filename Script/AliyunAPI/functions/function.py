import json
import numpy

from aliyun import aliyun_api
from functions import getValue


def return_date(beginDay, appcode, code='000001', timeType='day'):
    """
    获取可用日起序列
    :param beginDay: 开始时间
    :param appcode: appcode
    :param code: 三大代码
    :param timeType: 5/30/60/day/week/month
    :return: dateList
    """
    try:
        text = aliyun_api.mainindex(code, beginDay, timeType, appcode)
        all_dict = json.loads(text)
        dataList = all_dict['showapi_res_body']['dataList']
        dateList = []
        for data_element in dataList:
            #   dateList.insert(0, data_element['time'])
            dateList.append(data_element['time'])
        dateList.sort()
        return dateList
        # if int(dataList[0]['time']) < int(dataList[1]['time']):
        #     for data_element in dataList:
        #         #   dateList.insert(0, data_element['time'])
        #         dateList.append(data_element['time'])
        #     return dateList
        # else:
        #     for data_element in dataList:
        #         dateList.insert(0, data_element['time'])
        #         #   dateList.append(data_element['time'])
        #     return dateList
    except ValueError:
        return None


def return_stocklist(appcode):
    """
    获取代码列表，包含市场和名称
    :return: 
    """
    allmarket = ['sz', 'sh']
    stocklist = []
    mark = 1
    # texts = ''
    try:
        for market in allmarket:
            text = aliyun_api.stocklist(market, 1, appcode)
            # print(text)
            # 先读一次，获得总page数
            all_dict = json.loads(text)
            allpages = all_dict['showapi_res_body']['allPages']
            # texts = ''
            for currentPage in range(0, allpages):
                text = aliyun_api.stocklist(market, currentPage + 1, appcode)
                # texts+= text + '\n'
                # print(text)
                all_dict = json.loads(text)
                showapi_res_body = all_dict['showapi_res_body']
                newlist = showapi_res_body['contentlist']
                # print(newlist)
                exactPage = showapi_res_body['currentPage']
                # print(format(exactPage, 'd'))
                if exactPage != (currentPage + 1):
                    mark = 0
                    break
                pagelist = []
                for newlist_element in newlist:
                    tempdict = {'market': '', 'name': '', 'code': ''}
                    tempdict = {k: newlist_element[k] for k in tempdict}
                    if tempdict['code'][0] in ['0', '3', '6']:
                        pagelist.append(tempdict)
                stocklist.extend(pagelist)
                # print(stocklist)
            if mark != 1:
                break
        # return_value = [stocklist, texts]
        if mark == 1:
            return stocklist
            # return return_value
        else:
            return ValueError

    except ValueError:
        return None


def return_ssd(appcode):
    """
    获取每日非常规的代码列表
    :param appcode:
    :return:
    """
    try:
        text = aliyun_api.daily_ssd(appcode)
        all_dict = json.loads(text)
        showapi_res_body = all_dict['showapi_res_body']
        if getValue.get_DateTime()['fulldate'] == showapi_res_body['date']:
            return showapi_res_body
        else:
            return ValueError
    except ValueError:
        return None


def cal_boll(valueList, n, p):
    """
    计算布林三轨
    :param valueList:
    :param n:
    :param p:
    :return:
    """
    # valueList = [float(k) for k in valueList]
    valueList.reverse()
    boll = []
    for value in valueList:
        boll_dict = {}
        tempList = valueList[0:n]
        narray = numpy.array(tempList)
        mid = numpy.mean(narray)
        spd = numpy.sqrt(numpy.var(narray))
        upper = mid + p * spd
        lower = mid - p * spd
        boll_dict['mid'] = float(format(mid, '.2f'))
        boll_dict['upper'] = float(format(upper, '.2f'))
        boll_dict['lower'] = float(format(lower, '.2f'))
        # print(boll_dict)
        boll.insert(0, boll_dict)
        valueList.pop(0)
    return boll

