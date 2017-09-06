import time
import json
import numpy

from functions import function
from http_api import aliyun_api
from http_api import showapi_api
from http_api import QQ_api
from http_api import qtimq_api


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
    if getLength == 0:
        return dateList
    elif getLength < len(dateList):
        dateList = dateList[-getLength:]
        return dateList
    else:
        return dateList


def get_beginDate(ref_List, dateLenth, beginDate=''):
    if len(beginDate) == 8:
        ref_List['KbeginDay'] = beginDate
    elif not beginDate:
        if ref_List['KtimeType'] == '60':
            dateList = get_dateList('20170101', 50)
            ref_List['KbeginDay'] = dateList[-int(dateLenth / 4) - 1]
        elif ref_List['KtimeType'] == 'day':
            dateList = get_dateList('20150101', 400)
            ref_List['KbeginDay'] = dateList[-int(dateLenth) - 1]
        else:
            ref_List['KbeginDay'] = '20170101'
    else:
        pass
    return ref_List


def get_allCodelist(appcode='6a09e5fe3e724252b35d571a0b715baa'):
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
    try:
        delList.extend(ssdlist['newStockNetPublishList'])
        #   首发新股网上发行列表
        # delList.extend(ssdlist['stockholderList'])
        #   股东大会召开列表
        delList.extend(ssdlist['stopList'])
        #   停牌股票列表
        # delList.extend(ssdlist['addNewStockNetPublishList'])
        #   增发新股列表
        delList.extend(ssdlist['recoverList'])
        #   复牌股票列表
        # delList.extend(ssdlist['shareRegistList'])
        #   分红转增股权登记列表
        # delList.extend(ssdlist['ShareDividendList'])
        #   除权除息列表
        delList.extend(ssdlist['stockAlarmList'])
        #   退市风险警示列表
        delList.extend(ssdlist['startList'])
        #   新上市股票列表
    except KeyError:
        pass

    allCodelist = get_allCodelist(appcode)
    result = [k for k in allCodelist]

    for delCode in delList:
        # print(delCode)
        try:
            result.remove(delCode)
        except ValueError:
            pass
    return result


def get_blockList(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    detail_List = []
    element = {}
    allBlockDict = function.return_blockList(appcode)
    allBlockList = allBlockDict['showapi_res_body']['list']
    # print(allBlockList)
    # print('\n')
    for blockDict in allBlockList:
        # print(blockDict)
        blockList = blockDict['childList']
        "'申万行业'"
        "'概念板块'"
        "'地域板块'"
        "'证监会行业'"
        if blockDict['name'] == '概念板块':
            # print(blockDict['name']+'\n')
            for block in blockList:
                # print(block['name'] + '\t' + block['code'])
                element = {}
                element['name'] = block['name']
                element['code'] = block['code']
                detail_List.append(element)
        elif blockDict['name'] == '证监会行业':
            # print(blockDict['name']+'\n')
            for block in blockDict['childList']:
                for blockChild in block['childList']:
                    # print(blockChild['name'] + '\t' + blockChild['code'])
                    element = {}
                    element['name'] = blockChild['name']
                    element['code'] = blockChild['code']
                    detail_List.append(element)
        else:
            pass
        # print('\n\n')
    return detail_List


def get_blockList_showapi(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    仍旧使用的是旧的aliyun api
    :param appcode: 6a09e5fe3e724252b35d571a0b715baa
    :return:
    """
    detail_List = []
    element = {}
    allBlockDict = function.return_blockList_showapi(appcode)
    allBlockList = allBlockDict['showapi_res_body']['list']
    # print(allBlockList)
    # print('\n')
    for blockDict in allBlockList:
        # print(blockDict)
        blockList = blockDict['childList']
        "'申万行业'"
        "'概念板块'"
        "'地域板块'"
        "'证监会行业'"
        if blockDict['name'] == '概念板块':
            # print(blockDict['name']+'\n')
            for block in blockList:
                # print(block['name'] + '\t' + block['code'])
                element = {'name': block['name'], 'code': block['code']}
                detail_List.append(element)
                del element
        elif blockDict['name'] == '证监会行业':
            # print(blockDict['name']+'\n')
            # print(blockDict)
            for block in blockDict['childList']:
                for blockChild in block['childList']:
                    # print(blockChild['name'] + '\t' + blockChild['code'])
                    element = {'name': blockChild['name'], 'code': blockChild['code']}
                    detail_List.append(element)
                    del element
        # elif blockDict['name'] == '申万行业':
        #     # print(blockDict)
        #     # for block in blockDict['childList']:
        #     for blockChild in blockDict['childList']:
        #         # print(blockChild['name'] + '\t' + blockChild['code'])
        #         element = {'name': blockChild['name'], 'code': blockChild['code']}
        #         detail_List.append(element)
        #         del element
        else:
            pass
            # print('\n\n')
    return detail_List


def get_blockStocks_showapi(blockCode: object, appcode: object = '6a09e5fe3e724252b35d571a0b715baa') -> object:
    """
    获取板块内个股列表信息
    :param blockCode:
    :param appcode:
    :return:
    """
    return function.return_block_stocks(blockCode, appcode)


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


def get_dataList(api_input):
    """
    解析aliyun返回值的dataList
    :param api_input:
    :return:
    """
    dataList = api_input['showapi_res_body']['dataList']
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
    try:
        allkeys = list(allssd)
    except TypeError:
        allkeys = []
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
    # print(lhb_list)
    i = 0
    result = []
    for f in lhb_list:
        # print(f)
        i += 1
        if int(f['date']) <= 20150101:
            continue
        temp = True
        for temp1 in lhb_list[i:]:
            if f['code'] == temp1['code'] and f['date'] == temp1['date']:
                temp = False
                break
            temp = True
        if not temp:
            continue
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
        aliyun_str = aliyun_api.realtime(code, beginDay, '60', 'bfq', appcode)
        aliyun_dict = json.loads(aliyun_str)
        dataList = get_dataList(aliyun_dict)
        dataList.reverse()
        realtimeValue = []
        tempVol = 0
        tempOpen = None
        for element in dataList:
            # print(element)
            if element['minute'][-4:] == '0930':
                tempVol = int(element['volumn'])
                tempOpen = element['open']
            elif element['minute'][-4:] == '1030':
                realVol = format((int(element['volumn']) + tempVol), 'd')
                if tempOpen:
                    realOpen = tempOpen
                else:
                    realOpen = element['open']
                element['min'] = min(realOpen, element['min'])
                element['max'] = max(realOpen, element['max'])
                element['volumn'] = realVol
                element['open'] = realOpen
                realtimeValue.append(element)
                tempOpen = None
            else:
                realtimeValue.append(element)
        realtimeList = realtimeValue
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
        # print(closeList)
        # closeList.reverse()
        lastcloseList = [k for k in closeList]
        boll = function.cal_boll(closeList, n, p)
        m = len(boll)
        boll = boll[-m + 1:]
        realtimeList = realtimeList[-m + 1:]
        lastcloseList = lastcloseList[-m:]
        lastclose = {}
        for i in range(0, m - 1):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            lastclose['lastclose'] = lastcloseList[i]
            # print(realtimeList[i])
            realtimeList[i]['min'] = float(realtimeList[i]['min'])
            if len(realtimeList[i]['open']) == 0:
                realtimeList[i]['open'] = 0
            else:
                realtimeList[i]['open'] = float(realtimeList[i]['open'])
            realtimeList[i]['max'] = float(realtimeList[i]['max'])
            realtimeList[i]['close'] = float(realtimeList[i]['close'])
            realtimeList[i]['volumn'] = float(realtimeList[i]['volumn'])
            realtimeList[i].update(lastclose)
            realtimeList[i].update(boll[i])
            # print(realtimeList[i])
        # print(realtimeList)
        realtimeList = realtimeList[-getLength:]
        return realtimeList
    except ValueError:
        return None


def get_60F_showapi(code, beginDay, getLength, n=20, p=2, appcode='6a09e5fe3e724252b35d571a0b715baa'):
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
        showapi_str = showapi_api.realtime(code, beginDay, '60', 'bfq', appcode)
        # print(showapi_str)
        showapi_dict = json.loads(showapi_str)
        for i in range(10):
            try:
                if showapi_dict['showapi_res_body']['ret_code'] != 0:
                    print('Oh,Let me have a rest! 10S!')
                    time.sleep(10)
                else:
                    break
                showapi_str = showapi_api.realtime(code, beginDay, '60', 'bfq', appcode)
                showapi_dict = json.loads(showapi_str)
            except KeyError:
                print('Oh,Let me have a rest! 10S!')
                time.sleep(10)
                showapi_str = showapi_api.realtime(code, beginDay, '60', 'bfq', appcode)
                showapi_dict = json.loads(showapi_str)
        dataList = get_dataList(showapi_dict)
        dataList.reverse()
        realtimeValue = []
        tempVol = 0
        tempOpen = 0
        for element in dataList[:]:
            if element['minute'][-4:] == '0930':
                tempVol = float(element['volumn'])
                tempOpen = float(element['open'])
            elif element['minute'][-4:] == '1030':
                realVol = format((float(element['volumn']) + tempVol), 'f')
                if tempOpen:
                    realOpen = tempOpen
                else:
                    realOpen = float(element['open'])
                element['min'] = format(min(realOpen, float(element['min'])), 'f')
                element['max'] = format(max(realOpen, float(element['max'])), 'f')
                element['volumn'] = realVol
                element['open'] = format(realOpen, 'f')
                realtimeValue.append(element)
                tempOpen = 0
            else:
                realtimeValue.append(element)
        realtimeList = [k for k in realtimeValue]
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
        # print(closeList)
        # closeList.reverse()
        lastcloseList = [k for k in closeList]
        boll = function.cal_boll(closeList[:], n, p)
        boll144 = function.cal_boll_144(closeList[:])
        m = len(boll)
        n = len(boll144)
        m = min(m, n)
        # print('m len(boll) = ', end='')
        # print(m)
        # print('n len(boll144) = ', end='')
        # print(n)
        boll = boll[-m + 1:]
        boll144 = boll144[-m + 1:]
        realtimeList = realtimeList[-m + 1:]
        lastcloseList = lastcloseList[-m:]
        lastclose = {}
        if m == 1:
            lastclose['lastclose'] = float(realtimeList[0]['open'])
            realtimeList[0]['min'] = float(realtimeList[0]['min'])
            if len(realtimeList[0]['open']) == 0:
                realtimeList[0]['open'] = 0
            else:
                realtimeList[0]['open'] = float(realtimeList[0]['open'])
            realtimeList[0]['max'] = float(realtimeList[0]['max'])
            realtimeList[0]['close'] = float(realtimeList[0]['close'])
            realtimeList[0]['volumn'] = float(realtimeList[0]['volumn'])
            realtimeList[0].update(lastclose)
            realtimeList[0].update(boll[0])
            realtimeList[0].update(boll144[0])
        for i in range(0, m - 1):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            lastclose['lastclose'] = lastcloseList[i]
            realtimeList[i]['min'] = float(realtimeList[i]['min'])
            if len(realtimeList[i]['open']) == 0:
                realtimeList[i]['open'] = 0
            else:
                realtimeList[i]['open'] = float(realtimeList[i]['open'])
            realtimeList[i]['max'] = float(realtimeList[i]['max'])
            realtimeList[i]['close'] = float(realtimeList[i]['close'])
            realtimeList[i]['volumn'] = float(realtimeList[i]['volumn'])
            realtimeList[i].update(lastclose)
            realtimeList[i].update(boll[i])
            realtimeList[i].update(boll144[i])
            # print(realtimeList[i])
        # print(realtimeList)
        realtimeList = realtimeList[-getLength:]
        return realtimeList
    except ValueError:
        return None


def get_60F_qtimq(code, allLength, getLength, n=20, p=2):
    """
    获取指定日期长度的60F,
    同时计算boll
    :param allLength:
    :param p: p常量
    :param n: 布林计算天数
    :param code:
    :param getLength: = 2n / 4
    :return:
    """
    try:
        if len(code) == 6:
            if code[0] == '6':
                code = 'sh' + code
            elif code[0] == '0' or code[0] == '3':
                code = 'sz' + code
        elif len(code) == 8:
            code = code
        else:
            raise ValueError('Invalid code:', code)

        api_str = qtimq_api.realtime(code, allLength, '60')
        # print(api_str)
        api_dict = json.loads(api_str)
        # print(api_dict)
        for i in range(10):
            try:
                if api_dict['code'] != 0 or api_dict['msg'] != '':
                    print('Oh,Let me have a rest! 10S!')
                    time.sleep(10)
                else:
                    break
                api_str = qtimq_api.realtime(code, allLength, '60')
                api_dict = json.loads(api_str)
            except KeyError:
                print('Oh,Let me have a rest! 10S!')
                time.sleep(10)
                api_str = qtimq_api.realtime(code, allLength, '60')
                api_dict = json.loads(api_str)

        dataList = api_dict['data'][code]['m60']
        # dataList.reverse()
        realtimeValue = []
        # tempVol = 0
        # tempOpen = 0
        for element in dataList[:]:
            # if element['minute'][-4:] == '0930':
            #     tempVol = float(element['volumn'])
            #     tempOpen = float(element['open'])
            # elif element['minute'][-4:] == '1030':
            #     realVol = format((float(element['volumn']) + tempVol), 'f')
            #     if tempOpen:
            #         realOpen = tempOpen
            #     else:
            #         realOpen = float(element['open'])
            #     element['min'] = format(min(realOpen, float(element['min'])), 'f')
            #     element['max'] = format(max(realOpen, float(element['max'])), 'f')
            #     element['volumn'] = realVol
            #     element['open'] = format(realOpen, 'f')
            #     realtimeValue.append(element)
            #     tempOpen = 0
            # else:
            #     realtimeValue.append(element)
            tempDict = {
                            'time': element[0],
                            'minute': element[0],
                            'open': element[1],
                            'close': element[2],
                            'max': element[3],
                            'min': element[4],
                            'volumn': element[5],
                        }
            realtimeValue.append(tempDict)
        realtimeList = realtimeValue[:]
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
        # print(closeList)
        # closeList.reverse()
        lastcloseList = closeList[:]
        boll = function.cal_boll(closeList[:], n, p)
        boll55 = function.cal_boll_55(closeList[:])
        boll144 = function.cal_boll_144(closeList[:])
        m = len(boll)
        n = len(boll144)
        w = len(boll55)
        m = min(m, n, w)
        # print('m len(boll) = ', end='')
        # print(m)
        # print('n len(boll144) = ', end='')
        # print(n)
        boll = boll[-m + 1:]
        boll55 = boll55[-m + 1:]
        boll144 = boll144[-m + 1:]
        realtimeList = realtimeList[-m + 1:]
        lastcloseList = lastcloseList[-m:]
        lastclose = {}
        if m == 1:
            lastclose['lastclose'] = float(realtimeList[0]['open'])
            realtimeList[0]['min'] = float(realtimeList[0]['min'])
            if len(realtimeList[0]['open']) == 0:
                realtimeList[0]['open'] = 0
            else:
                realtimeList[0]['open'] = float(realtimeList[0]['open'])
            realtimeList[0]['max'] = float(realtimeList[0]['max'])
            realtimeList[0]['close'] = float(realtimeList[0]['close'])
            realtimeList[0]['volumn'] = float(realtimeList[0]['volumn'])
            realtimeList[0].update(lastclose)
            realtimeList[0].update(boll[0])
            realtimeList[0].update(boll55[0])
            realtimeList[0].update(boll144[0])
        for i in range(0, m - 1):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            lastclose['lastclose'] = lastcloseList[i]
            realtimeList[i]['min'] = float(realtimeList[i]['min'])
            if len(realtimeList[i]['open']) == 0:
                realtimeList[i]['open'] = 0
            else:
                realtimeList[i]['open'] = float(realtimeList[i]['open'])
            realtimeList[i]['max'] = float(realtimeList[i]['max'])
            realtimeList[i]['close'] = float(realtimeList[i]['close'])
            realtimeList[i]['volumn'] = float(realtimeList[i]['volumn'])
            realtimeList[i].update(lastclose)
            realtimeList[i].update(boll[i])
            realtimeList[i].update(boll55[i])
            realtimeList[i].update(boll144[i])
            # print(realtimeList[i])
        # print(realtimeList)
        realtimeList = realtimeList[-getLength:]
        return realtimeList
    except ValueError:
        return None


def get_dayK(code, beginDay, getLength, n=20, p=2, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
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
        aliyun_str = aliyun_api.realtime(code, beginDay, 'day', 'bfq', appcode)
        aliyun_dict = json.loads(aliyun_str)
        dataList = get_dataList(aliyun_dict)
        dataList.reverse()
        realtimeList = [k for k in dataList]
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
        # print(closeList)
        # closeList.reverse()
        lastcloseList = [k for k in closeList]
        boll = function.cal_boll(closeList, n, p)
        m = len(boll)
        boll = boll[-m + 1:]
        realtimeList = realtimeList[-m + 1:]
        lastcloseList = lastcloseList[-m:]
        lastclose = {}
        for i in range(0, m - 1):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            lastclose['lastclose'] = lastcloseList[i]
            realtimeList[i]['min'] = float(realtimeList[i]['min'])
            if len(realtimeList[i]['open']) == 0:
                realtimeList[i]['open'] = 0
            else:
                realtimeList[i]['open'] = float(realtimeList[i]['open'])
            realtimeList[i]['max'] = float(realtimeList[i]['max'])
            realtimeList[i]['close'] = float(realtimeList[i]['close'])
            realtimeList[i]['volumn'] = float(realtimeList[i]['volumn'])
            realtimeList[i].update(lastclose)
            realtimeList[i].update(boll[i])
            # print(realtimeList[i])
        # print(realtimeList)
        realtimeList = realtimeList[-getLength:]
        return realtimeList
    except ValueError:
        return None


def get_dayK_showapi(code, beginDay, getLength, n=20, p=2, appcode='6a09e5fe3e724252b35d571a0b715baa'):
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
        showapi_str = showapi_api.realtime(code, beginDay, 'day', 'bfq', appcode)
        showapi_dict = json.loads(showapi_str)
        for i in range(10):
            try:
                if showapi_dict['showapi_res_body']['ret_code'] != 0:
                    print('Oh,Let me have a rest! 10S!')
                    time.sleep(10)
                else:
                    break
                showapi_str = showapi_api.realtime(code, beginDay, 'day', 'bfq', appcode)
                showapi_dict = json.loads(showapi_str)
            except KeyError:
                print('Oh,Let me have a rest! 10S!')
                time.sleep(10)
                showapi_str = showapi_api.realtime(code, beginDay, 'day', 'bfq', appcode)
                showapi_dict = json.loads(showapi_str)
        dataList = get_dataList(showapi_dict)
        dataList.reverse()
        realtimeList = [k for k in dataList]
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
        # print(closeList)
        # closeList.reverse()
        lastcloseList = [k for k in closeList]
        boll = function.cal_boll(closeList[:], n, p)
        boll144 = function.cal_boll_144(closeList[:])
        m = len(boll)
        n = len(boll144)
        m = min(m, n)
        # print('m len(boll) = ', end='')
        # print(m)
        # print('n len(boll144) = ', end='')
        # print(n)
        boll = boll[-m + 1:]
        boll144 = boll144[-m + 1:]
        realtimeList = realtimeList[-m + 1:]
        lastcloseList = lastcloseList[-m:]
        lastclose = {}
        if m == 1:
            lastclose['lastclose'] = float(realtimeList[0]['open'])
            realtimeList[0]['min'] = float(realtimeList[0]['min'])
            if len(realtimeList[0]['open']) == 0:
                realtimeList[0]['open'] = 0
            else:
                realtimeList[0]['open'] = float(realtimeList[0]['open'])
            realtimeList[0]['max'] = float(realtimeList[0]['max'])
            realtimeList[0]['close'] = float(realtimeList[0]['close'])
            realtimeList[0]['volumn'] = float(realtimeList[0]['volumn'])
            realtimeList[0].update(lastclose)
            realtimeList[0].update(boll[0])
            realtimeList[0].update(boll144[0])
        for i in range(0, m - 1):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            lastclose['lastclose'] = lastcloseList[i]
            realtimeList[i]['min'] = float(realtimeList[i]['min'])
            if len(realtimeList[i]['open']) == 0:
                realtimeList[i]['open'] = 0
            else:
                realtimeList[i]['open'] = float(realtimeList[i]['open'])
            realtimeList[i]['max'] = float(realtimeList[i]['max'])
            realtimeList[i]['close'] = float(realtimeList[i]['close'])
            realtimeList[i]['volumn'] = float(realtimeList[i]['volumn'])
            realtimeList[i].update(lastclose)
            realtimeList[i].update(boll[i])
            realtimeList[i].update(boll144[i])
            # print(realtimeList[i])
        # print(realtimeList)
        realtimeList = realtimeList[-getLength:]
        return realtimeList
    except ValueError:
        return None


def get_dayK_qtimq(code, allLength, getLength, n=20, p=2):
    """
    获取指定日期长度的60F,
    同时计算boll
    :param allLength:
    :param p: p常量
    :param n: 布林计算天数
    :param code:
    :param getLength: = 2n / 4
    :return:
    """
    try:
        if len(code) == 6:
            if code[0] == '6':
                code = 'sh' + code
            elif code[0] == '0' or code[0] == '3':
                code = 'sz' + code
        elif len(code) == 8:
            code = code
        else:
            raise ValueError('Invalid code:', code)

        api_str = qtimq_api.realtime(code, allLength, 'day')
        api_dict = json.loads(api_str)
        for i in range(10):
            try:
                if api_dict['code'] != 0 or api_dict['msg'] != '':
                    print('Oh,Let me have a rest! 10S!')
                    time.sleep(10)
                else:
                    break
                api_str = qtimq_api.realtime(code, allLength, 'day')
                api_dict = json.loads(api_str)
            except KeyError:
                print('Oh,Let me have a rest! 10S!')
                time.sleep(10)
                api_str = qtimq_api.realtime(code, allLength, 'day')
                api_dict = json.loads(api_str)

        dataList = api_dict['data'][code]['day']
        # dataList.reverse()
        realtimeValue = []
        for element in dataList[:]:
            # if element['minute'][-4:] == '0930':
            #     tempVol = float(element['volumn'])
            #     tempOpen = float(element['open'])
            # elif element['minute'][-4:] == '1030':
            #     realVol = format((float(element['volumn']) + tempVol), 'f')
            #     if tempOpen:
            #         realOpen = tempOpen
            #     else:
            #         realOpen = float(element['open'])
            #     element['min'] = format(min(realOpen, float(element['min'])), 'f')
            #     element['max'] = format(max(realOpen, float(element['max'])), 'f')
            #     element['volumn'] = realVol
            #     element['open'] = format(realOpen, 'f')
            #     realtimeValue.append(element)
            #     tempOpen = 0
            # else:
            #     realtimeValue.append(element)
            tempDict = {
                'time': element[0].replace('-', ''),
                'open': element[1],
                'close': element[2],
                'max': element[3],
                'min': element[4],
                'volumn': element[5],
            }
            realtimeValue.append(tempDict)
        realtimeList = realtimeValue[:]
        closeList = []
        for element in realtimeList:
            closeList.append(float(element['close']))
        # print(closeList)
        # closeList.reverse()
        lastcloseList = closeList[:]
        boll = function.cal_boll(closeList[:], n, p)
        boll55 = function.cal_boll_55(closeList[:])
        boll144 = function.cal_boll_144(closeList[:])
        m = len(boll)
        n = len(boll144)
        w = len(boll55)
        m = min(m, n, w)
        # print('m len(boll) = ', end='')
        # print(m)
        # print('n len(boll144) = ', end='')
        # print(n)
        boll = boll[-m + 1:]
        boll55 = boll55[-m + 1:]
        boll144 = boll144[-m + 1:]
        realtimeList = realtimeList[-m + 1:]
        lastcloseList = lastcloseList[-m:]
        lastclose = {}
        if m == 1:
            lastclose['lastclose'] = float(realtimeList[0]['open'])
            realtimeList[0]['min'] = float(realtimeList[0]['min'])
            if len(realtimeList[0]['open']) == 0:
                realtimeList[0]['open'] = 0
            else:
                realtimeList[0]['open'] = float(realtimeList[0]['open'])
            realtimeList[0]['max'] = float(realtimeList[0]['max'])
            realtimeList[0]['close'] = float(realtimeList[0]['close'])
            realtimeList[0]['volumn'] = float(realtimeList[0]['volumn'])
            realtimeList[0].update(lastclose)
            realtimeList[0].update(boll[0])
            realtimeList[0].update(boll55[0])
            realtimeList[0].update(boll144[0])
        for i in range(0, m - 1):
            # realtimeList[i]['mid', 'upper', 'lower'] = boll[i]['mid', 'upper', 'lower']
            lastclose['lastclose'] = lastcloseList[i]
            realtimeList[i]['min'] = float(realtimeList[i]['min'])
            if len(realtimeList[i]['open']) == 0:
                realtimeList[i]['open'] = 0
            else:
                realtimeList[i]['open'] = float(realtimeList[i]['open'])
            realtimeList[i]['max'] = float(realtimeList[i]['max'])
            realtimeList[i]['close'] = float(realtimeList[i]['close'])
            realtimeList[i]['volumn'] = float(realtimeList[i]['volumn'])
            realtimeList[i].update(lastclose)
            realtimeList[i].update(boll[i])
            realtimeList[i].update(boll55[i])
            realtimeList[i].update(boll144[i])
            # print(realtimeList[i])
        # print(realtimeList)
        realtimeList = realtimeList[-getLength:]
        return realtimeList
    except ValueError:
        return None


def get_timeLine(code, dayLength, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    try:
        result = function.return_timeline(code, format(dayLength, 'd'), appcode)
    except ValueError:
        return None
    else:
        return result


def get_timeLine_qtimq(code):
    if len(code) == 6:
        if code[0] == '6':
            code = 'sh' + code
        elif code[0] == '0' or code[0] == '3':
            code = 'sz' + code
    elif len(code) == 8:
        code = code
    else:
        raise ValueError('Invalid code:', code)

    try:
        result = function.return_timeline_qtimq(code)
    except ValueError:
        return None
    else:
        return result


def add_index(code):
    """
    输入6位代码，输出带主板的代码
    :param code:
    :return:
    """
    if code[0] == '6':
        code_text = code + '.sh'
    elif code[0] == '0' or code[0] == '3':
        code_text = code + '.sz'
    else:
        code_text = ''
    return code_text
