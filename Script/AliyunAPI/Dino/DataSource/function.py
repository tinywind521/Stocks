import json
import numpy
import time
import sys

from http_api import aliyun_api, showapi_api, qtimq_api
from functions import getValue
from stock_Class.stock import Stock, Yline


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
        # print(tempArg['result']['101_20BollDay4B'])
        if tempArg['result']['001_144BollUpper20BollUpside']['结果'] == 1:
            objResult.setResultAppend('001', tempArg)
        # if tempArg['result']['002_20DayBollRaiseAndHoriLevel']['结果'] == 1:
        #     objResult.setResultAppend('002', tempArg)
        # if tempArg['result']['003_Day9Bears']['结果'] == 1:
        #     objResult.setResultAppend('003', tempArg)
        # if tempArg['result']['101_20BollDay4B']['结果'] == 1 and tempArg['value'] >= 90:
        if tempArg['result']['101_20BollDay4B']['结果'] == 1\
                and tempArg['result']['101_20BollDay4B']['前期最大涨幅'] >= 10:
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
            # print(s.Kvalue[-1])
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
        # print('结果', ': ', tempArg['result']['101_20Boll60F4B']['结果'])
        # print('结果', ': ', tempArg['result']['101_20BollDay4B']['结果'])
        # print('中轨状态', ': ', tempArg['result']['101_20Boll60F4B']['中轨状态'])
        # print('中轨状态', ': ', tempArg['result']['101_20BollDay4B']['中轨状态'])
        # print('K线位于20布林位置', ': ', tempArg['result']['101_20Boll60F4B']['K线位于20布林位置'])
        # print('K线位于20布林位置', ': ', tempArg['result']['101_20BollDay4B']['K线位于20布林位置'])
        # print('回调次数', ': ', tempArg['result']['101_20Boll60F4B']['回调次数'])
        # print('回调次数', ': ', tempArg['result']['101_20BollDay4B']['回调次数'])
        # print('层级差得分', ': ', tempArg['result']['101_20Boll60F4B']['层级差得分'])
        # print('层级差得分', ': ', tempArg['result']['101_20BollDay4B']['层级差得分'])
        # print('阳线占比', ': ', tempArg['result']['101_20Boll60F4B']['阳线占比'])
        # print('阳线占比', ': ', tempArg['result']['101_20BollDay4B']['阳线占比'])
        if tempArg['result']['101_20Boll60F4B']['结果'] == 1:
            # print('第一轮判断')
            if ((tempArg['result']['101_20BollDay4B']['K线位于20布林位置'] >= 1
                 and tempArg['result']['101_20BollDay4B']['回调次数'] == 0)
                or (2 >= tempArg['result']['101_20BollDay4B']['K线位于20布林位置'] >= -1
                    and tempArg['result']['101_20BollDay4B']['回调次数'] == 1)
                    or (2 >= tempArg['result']['101_20BollDay4B']['K线位于20布林位置'] >= 1
                        and tempArg['result']['101_20BollDay4B']['回调次数'] == 2))\
                \
                    and ((2 >= tempArg['result']['101_20Boll60F4B']['K线位于20布林位置'] >= 1
                          and 1 <= tempArg['result']['101_20Boll60F4B']['回调次数'] <= 2)
                         or (tempArg['result']['101_20Boll60F4B']['K线位于20布林位置'] >= -1
                             and tempArg['result']['101_20Boll60F4B']['回调次数'] == 0))\
                \
                    and ((tempArg['result']['101_20BollDay4B']['中轨状态'] == 0
                         and tempArg['result']['101_20Boll60F4B']['中轨状态'] >= 1)
                         or (tempArg['result']['101_20BollDay4B']['中轨状态'] >= 1
                             and tempArg['result']['101_20Boll60F4B']['中轨状态'] >= 0)) \
                    and ((tempArg['result']['101_20BollDay4B']['近期最大涨幅'] >= 3
                          and tempArg['result']['101_20BollDay4B']['回调次数'] == 0)
                         or (tempArg['result']['101_20BollDay4B']['近期最大涨幅'] >= 8
                             and 2 >= tempArg['result']['101_20BollDay4B']['回调次数'] >= 1
                             and tempArg['result']['101_20BollDay4B']['近期最高位置'] >= 2)):
                # print('第二轮判断')
                # if tempArg['result']['101_20BollDay4B']['阳线占比'] >= 50 \
                #         and (tempArg['result']['101_20BollDay4B']['层级差得分'] >= 90
                #              or tempArg['result']['101_20BollDay4B']['层级差得分'] == 0):
                #     objResult.setResultAppend('101', tempArg)
                # elif tempArg['result']['101_20BollDay4B']['阳线占比'] >= 30 \
                #         and (tempArg['result']['101_20BollDay4B']['层级差得分'] >= 92.5
                #              or tempArg['result']['101_20BollDay4B']['层级差得分'] == 0):
                #     objResult.setResultAppend('101', tempArg)
                # else:
                #     pass
                if tempArg['result']['101_20BollDay4B']['层级差得分'] >= 90 \
                        or tempArg['result']['101_20BollDay4B']['层级差得分'] == 0:
                    objResult.setResultAppend('101', tempArg)
        del tempArg
    else:
        pass
