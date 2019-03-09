import time
import json
import numpy


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

    for i in range(10):
        try:
            if api_dict['code'] != 0 or api_dict['msg'] != '':
                print('Oh,Let me have a rest! 10S!')
                time.sleep(5)
            else:
                break
            api_str = qtimq_api.timeline5Days(code)
            api_dict = json.loads(api_str)
        except KeyError:
            print('Oh,Let me have a rest! 10S!')
            time.sleep(5)
            api_str = qtimq_api.timeline5Days(code)
            api_dict = json.loads(api_str)

    try:
        result = function.return_timeline_qtimq(code)
    except ValueError:
        return None
    else:
        return result


def get_timeLine5Days_qtimq(code):
    """
    获取五日分时
    :param code:
    :return:
    """
    if len(code) == 6:
        if code[0] == '6':
            code = 'sh' + code
        elif code[0] == '0' or code[0] == '3':
            code = 'sz' + code
    elif len(code) == 8:
        code = code
    else:
        raise ValueError('Invalid code:', code)

    api_str = qtimq_api.timeline5Days(code)
    api_dict = json.loads(api_str)
    for i in range(10):
        try:
            if api_dict['code'] != 0 or api_dict['msg'] != '':
                print('Oh,Let me have a rest! 10S!')
                time.sleep(5)
            else:
                break
            api_str = qtimq_api.timeline5Days(code)
            api_dict = json.loads(api_str)
        except KeyError:
            print('Oh,Let me have a rest! 10S!')
            time.sleep(5)
            api_str = qtimq_api.timeline5Days(code)
            api_dict = json.loads(api_str)
    try:
        all_dict = json.loads(api_str)
        showapi_res_body = all_dict['data']
        dataList = showapi_res_body[code]
        datesList = dataList['data']
        if not datesList:
            return None
        result = []
        for dateValue in datesList:
            # print('dateValue\t', dateValue)
            dateTemp = dateValue['date']
            dataTemp = dateValue['data']
            timeList = []
            lastVol = 0
            for timeElement in dataTemp:
                if timeElement:
                    timeArray = timeElement.split(' ')
                    totalVolumn = int(timeArray[2])
                    volumn = totalVolumn - lastVol
                    lastVol = totalVolumn
                    timeDict = {'time': timeArray[0], 'nowPrice': float(timeArray[1]), 'volume': volumn}
                    timeList.append(timeDict)
            timeList = timeList[2:-1]
            result.append({dateTemp: timeList})
        # print(code, [k['date'] for k in datesList])
        return result
    except (ValueError, TypeError):
        print('\nError Value: ', all_dict)
        return None


def get_timeLine3Days_qtimq(code):
    """
    获取3日分时
    :param code:
    :return:
    """
    if len(code) == 6:
        if code[0] == '6':
            code = 'sh' + code
        elif code[0] == '0' or code[0] == '3':
            code = 'sz' + code
    elif len(code) == 8:
        code = code
    else:
        raise ValueError('Invalid code:', code)

    api_str = qtimq_api.timeline5Days(code)
    api_dict = json.loads(api_str)
    for i in range(10):
        try:
            if api_dict['code'] != 0 or api_dict['msg'] != '':
                print('Oh,Let me have a rest! 10S!')
                time.sleep(5)
            else:
                break
            api_str = qtimq_api.timeline5Days(code)
            api_dict = json.loads(api_str)
        except KeyError:
            print('Oh,Let me have a rest! 10S!')
            time.sleep(5)
            api_str = qtimq_api.timeline5Days(code)
            api_dict = json.loads(api_str)
    try:
        all_dict = json.loads(api_str)
        showapi_res_body = all_dict['data']
        dataList = showapi_res_body[code]
        datesList = dataList['data']
        if not datesList:
            return None
        result = []
        for dateValue in datesList:
            # print('dateValue\t', dateValue)
            dateTemp = dateValue['date']
            dataTemp = dateValue['data']
            timeList = []
            lastVol = 0
            for timeElement in dataTemp:
                if timeElement:
                    timeArray = timeElement.split(' ')
                    totalVolumn = int(timeArray[2])
                    volumn = totalVolumn - lastVol
                    lastVol = totalVolumn
                    timeDict = {'time': timeArray[0], 'nowPrice': float(timeArray[1]), 'volume': volumn}
                    timeList.append(timeDict)
            # timeList = timeList[2:-1]
            result.append({dateTemp: timeList})
        # print(code, [k['date'] for k in datesList])
        return result[0:3]
    except (ValueError, TypeError):
        print('\nError Value: ', all_dict)
        return None


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
