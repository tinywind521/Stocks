import json
import numpy
import time
import sys

from http_api import aliyun_api, showapi_api, qtimq_api
from functions import getValue
from stock_Class.stock import Stock, Yline, ResultDeal


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
        text = showapi_api.mainindex(code, beginDay, timeType, appcode)
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
            text = showapi_api.stocklist(market, 1, appcode)
            # print(text)
            # 先读一次，获得总page数
            all_dict = json.loads(text)
            showapi_res_body = all_dict['showapi_res_body']
            # print(showapi_res_body)
            for i in range(10):
                try:
                    if showapi_res_body['maxResult'] != 50:
                        print('Oh,Let me have a rest! 10S!')
                        time.sleep(10)
                    else:
                        break
                    text = showapi_api.stocklist(market, 1, appcode)
                    all_dict = json.loads(text)
                    showapi_res_body = all_dict['showapi_res_body']
                except KeyError:
                    print('Oh,Let me have a rest! 10S!')
                    time.sleep(10)
                    text = showapi_api.stocklist(market, 1, appcode)
                    all_dict = json.loads(text)
                    showapi_res_body = all_dict['showapi_res_body']
            allpages = showapi_res_body['allPages']
            newlist = showapi_res_body['contentlist']
            print(format(allpages, 'd'))
            pagelist = []
            for newlist_element in newlist:
                tempdict = {'market': '', 'name': '', 'code': ''}
                tempdict = {k: newlist_element[k] for k in tempdict}
                if tempdict['code'][0] in ['0', '3', '6']:
                    pagelist.append(tempdict)
            stocklist.extend(pagelist)
            # print(stocklist)
            if allpages >= 2:
                for currentPage in range(1, allpages):
                    text = showapi_api.stocklist(market, currentPage + 1, appcode)
                    # print(text)
                    all_dict = json.loads(text)
                    showapi_res_body = all_dict['showapi_res_body']
                    # print(showapi_res_body['maxResult'])
                    for i in range(10):
                        try:
                            if showapi_res_body['maxResult'] != 50:
                                print('Oh,Let me have a rest! 10S!')
                                time.sleep(10)
                            else:
                                break
                            text = showapi_api.stocklist(market, currentPage + 1, appcode)
                            all_dict = json.loads(text)
                            showapi_res_body = all_dict['showapi_res_body']
                        except KeyError:
                            print('Oh,Let me have a rest! 10S!')
                            time.sleep(10)
                            text = showapi_api.stocklist(market, currentPage + 1, appcode)
                            all_dict = json.loads(text)
                            showapi_res_body = all_dict['showapi_res_body']
                    newlist = showapi_res_body['contentlist']
                    # print(newlist)
                    exactPage = showapi_res_body['currentPage']
                    print(format(allpages - exactPage, 'd'))
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


def return_blockList(appcode):
    text = aliyun_api.block_list(appcode)
    # print(text)
    # 先读一次，获得总page数
    all_dict = json.loads(text)
    return all_dict


def return_blockList_showapi(appcode):
    text = showapi_api.block_list(appcode)
    # print(text)
    # 先读一次，获得总page数
    all_dict = json.loads(text)
    return all_dict


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
    valueList.reverse()
    valueTemp = [float(k) for k in valueList]
    boll = []
    for value in valueList:
        boll_dict = {}
        if len(valueTemp) >= 20:
            tempList = valueTemp[0:n]
            narray = numpy.array(tempList)
            mid = numpy.mean(narray)
            spd = numpy.sqrt(numpy.var(narray))
            upper = mid + p * spd
            lower = mid - p * spd
            boll_dict['mid'] = float(format(mid, '.2f'))
            boll_dict['upper'] = float(format(upper, '.2f'))
            boll_dict['lower'] = float(format(lower, '.2f'))
        else:
            boll_dict['mid'] = 0
            boll_dict['upper'] = 0
            boll_dict['lower'] = 0
        # print(boll_dict)
        boll.insert(0, boll_dict)
        valueTemp.pop(0)
    return boll


def cal_boll_144(valueList, n=144, p=2):
    """
    计算144布林三轨
    :param valueList:
    :param n:
    :param p:
    :return:
    """
    valueList.reverse()
    valueTemp = [float(k) for k in valueList]
    boll = []
    for value in valueList:
        boll_dict = {}
        if len(valueTemp) >= 144:
            tempList = valueTemp[0:n]
            narray = numpy.array(tempList)
            mid = numpy.mean(narray)
            spd = numpy.sqrt(numpy.var(narray))
            upper = mid + p * spd
            lower = mid - p * spd
            boll_dict['mid144'] = float(format(mid, '.2f'))
            boll_dict['upper144'] = float(format(upper, '.2f'))
            boll_dict['lower144'] = float(format(lower, '.2f'))
        else:
            boll_dict['mid144'] = 0
            boll_dict['upper144'] = 0
            boll_dict['lower144'] = 0
        # print(boll_dict)
        boll.insert(0, boll_dict)
        valueTemp.pop(0)
    return boll


def return_block_stocks(blockID, appcode):
    """
    获取板块内列表
    :return:
    """
    block_stocksList = []
    block_stocks = {}
    mark = 1
    # texts = ''
    try:
        text = showapi_api.block_stocks(blockID, 1, appcode)
        # print(text)
        # 先读一次，获得总page数
        all_dict = json.loads(text)
        for i in range(10):
            try:
                if all_dict['showapi_res_body']['ret_code'] != 0:
                    print('Oh,Let me have a rest! 10S!')
                    time.sleep(10)
                else:
                    break
                text = showapi_api.block_stocks(blockID, 1, appcode)
                all_dict = json.loads(text)
            except KeyError:
                print('Oh,Let me have a rest! 10S!')
                time.sleep(10)
                text = showapi_api.block_stocks(blockID, 1, appcode)
                all_dict = json.loads(text)
        pagebean = all_dict['showapi_res_body']['pagebean']
        allpages = pagebean['allPages']
        if allpages:
            # print(pagebean)
            block_stocks['name'] = pagebean['name']
            newlist = pagebean['contentlist']
            # print(newlist)
            # print(format(exactPage, 'd'))
            pagelist = []
            for newlist_element in newlist:
                # tempdict = {'market': '', 'name': '', 'code': ''}
                # tempdict = {k: newlist_element[k] for k in tempdict}
                if newlist_element['code'][0] in ['0', '3', '6']:
                    pagelist.append(newlist_element['code'])
            block_stocksList.extend(pagelist)
            # print(allpages)
            if allpages >= 2:
                for currentPage in range(1, allpages):
                    text = showapi_api.block_stocks(blockID, currentPage + 1, appcode)
                    # print(text)
                    all_dict = json.loads(text)
                    for i in range(10):
                        try:
                            if all_dict['showapi_res_body']['ret_code'] != 0:
                                print('Oh,Let me have a rest! 10S!')
                                time.sleep(10)
                            else:
                                break
                            text = showapi_api.block_stocks(blockID, currentPage + 1, appcode)
                            all_dict = json.loads(text)
                        except KeyError:
                            print('Oh,Let me have a rest! 10S!')
                            time.sleep(10)
                            text = showapi_api.block_stocks(blockID, currentPage + 1, appcode)
                            all_dict = json.loads(text)
                    pagebean = all_dict['showapi_res_body']['pagebean']
                    newlist = pagebean['contentlist']
                    # print(newlist)
                    exactPage = pagebean['currentPage']
                    # print(format(exactPage, 'd'))
                    if exactPage != (currentPage + 1):
                        mark = 0
                        break
                    pagelist = []
                    for newlist_element in newlist:
                        # tempdict = {'market': '', 'name': '', 'code': ''}
                        # tempdict = {k: newlist_element[k] for k in tempdict}
                        if newlist_element['code'][0] in ['0', '3', '6']:
                            pagelist.append(newlist_element['code'])
                    block_stocksList.extend(pagelist)
                    # print(block_stocksList)
                # return_value = [stocklist, texts]
        else:
            mark = 0
        if mark == 1:
            block_stocks['block_stocksList'] = block_stocksList
            return block_stocks
            # return return_value
        else:
            return None

    except ValueError:
        return None


def return_timeline(code, day, appcode):
    try:
        result = []
        text = aliyun_api.timeline(code, day, appcode)
        all_dict = json.loads(text)
        # print(all_dict)
        showapi_res_body = all_dict['showapi_res_body']
        dataList = showapi_res_body['dataList']
        # print(dataList)
        for dataElement in dataList:
            # print(dataElement)
            temp = dict()
            temp['date'] = dataElement['date']
            temp['lastclose'] = dataElement['yestclose']
            # length = dataElement['count']
            timeline = dataElement['minuteList']
            # print(len(timeline))
            # print(length)
            temp['timeline'] = timeline
            # if len(timeline) == int(length):
            #     temp['timeline'] = timeline
            # else:
            #     temp['timeline'] = None
            #     for ss in timeline:
            #         print(ss)
            result.append(temp)
        return result
    except ValueError:
        return None


def return_timeline_qtimq(code):
    try:
        result = []
        text = qtimq_api.timeline(code)
        all_dict = json.loads(text)
        # print(all_dict)
        showapi_res_body = all_dict['data']
        dataList = showapi_res_body[code]
        # print(dataList)
        temp = dict()
        temp['date'] = dataList['data']['date']
        timeLine = dataList['data']['data']
        timeList = []
        for timeElement in timeLine:
            timeArray = timeElement.split(' ')
            # timeKeys = ('time', 'nowPrice', 'volume')
            timeDict = {'time': timeArray[0], 'nowPrice': timeArray[1], 'volume': timeArray[2]}
            timeList.append(timeDict)
        temp['timeline'] = timeList
        result = temp
        return result
    except ValueError:
        return None


def view_bar(num, total, codeIn=''):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    r = '\r[%s%s] %2.2f%% %d/%d %s' % ("|"*flow, " "*(100-flow), rate_num, num, total, codeIn,)
    sys.stdout.write(r)
    sys.stdout.flush()


def calDayStatus(obj):
    codeArg = obj['codeArg']
    objResult = obj['objResult']
    ref_List = obj['ref_List']
    tempArg = {'code': '', 'value': 0, 'result': {'001_144BollUpper20BollUpside': {}}}
    s = Stock(codeArg, ref_List)
    while True:
        try:
            s.get_KValue()
            s.update_Kstatus()
            len(s.Kvalue)
            break
        except (TypeError, IndexError):
            time.sleep(5)
    if len(s.Kvalue) >= 5:
        try:
            y = Yline(s.Kvalue, None)
        except ValueError:
            return
        y.cal_patternResult(ref_List['KtimeType'])
        tempArg['code'] = codeArg
        tempArg['value'] = round(y.status, 3)
        tempArg['result'] = y.patternResult
        # print(codeArg)
        if tempArg['result']['001_144BollUpper20BollUpside']['结果'] == 1:
            objResult.setResultAppend('001', tempArg)
        if tempArg['result']['101_20BollDay4B']['结果'] == 1:
            objResult.setResultAppend('101', tempArg)
        del tempArg
    else:
        pass


def cal60FStatus(obj):
    element = obj['element']
    objResult = obj['objResult']
    ref_List = obj['ref_List']
    tempArg = {'code': '', 'valueDay': 0, 'value60F': 0, 'result': {'101_20Boll60F4B': {'结果': 0}}}
    s = Stock(element['code'], ref_List)
    while True:
        try:
            s.get_KValue()
            s.update_Kstatus()
            len(s.Kvalue)
            break
        except TypeError:
            time.sleep(5)
    if len(s.Kvalue) >= 5:
        try:
            y = Yline(s.Kvalue, None)
        except ValueError:
            return
        y.cal_patternResult(ref_List['KtimeType'])
        tempArg['code'] = element['code']
        tempArg['valueDay'] = element['value']
        tempArg['value60F'] = round(y.status, 3)
        # print(element['result'])
        # print({'101_20Boll60F4B': y.patternResult['101_20Boll60F4B']})
        if y.patternResult:
            tempdict = element['result']
            tempdict.update({'101_20Boll60F4B': y.patternResult['101_20Boll60F4B']})
            tempArg['result'] = tempdict
        else:
            tempArg['result']['101_20Boll60F4B']['结果'] = 0
        # print(tempArg['code'], tempArg['result'])
        # print(tempArg['result'])
        """
        中轨以上，回调次数放宽；
        中轨及其下方，只接受一次调整，以确保B3/4以及回撤后的二次启动。
        """
        if tempArg['result']['101_20Boll60F4B']['结果'] == 1:
            if (tempArg['result']['101_20BollDay4B']['K线位于20布林位置'] >= 1
                or (1 > tempArg['result']['101_20BollDay4B']['K线位于20布林位置'] >= -1
                    and tempArg['result']['101_20BollDay4B']['回调次数'] == 1)) \
                    and (2 >= tempArg['result']['101_20Boll60F4B']['K线位于20布林位置'] >= 1
                         or (1 > tempArg['result']['101_20Boll60F4B']['K线位于20布林位置'] >= -1
                             and tempArg['result']['101_20Boll60F4B']['回调次数'] == 1))\
                    and tempArg['result']['101_20BollDay4B']['中轨状态'] >= 0 \
                    and tempArg['result']['101_20Boll60F4B']['中轨状态'] == 1:
                if tempArg['result']['101_20Boll60F4B']['阳线占比'] >= 50 \
                        and (tempArg['result']['101_20Boll60F4B']['层级差得分'] >= 90
                             or tempArg['result']['101_20Boll60F4B']['层级差得分'] == 0):
                    objResult.setResultAppend('101', tempArg)
                elif tempArg['result']['101_20Boll60F4B']['阳线占比'] >= 30 \
                        and (tempArg['result']['101_20Boll60F4B']['层级差得分'] >= 92
                             or tempArg['result']['101_20Boll60F4B']['层级差得分'] == 0):
                    objResult.setResultAppend('101', tempArg)
                else:
                    pass
        del tempArg
    else:
        pass
