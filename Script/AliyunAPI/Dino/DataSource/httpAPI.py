import urllib.request
import urllib.error
import socket
import numpy
import time
import json
import tushare as ts
import pandas as pd


class DataTuShare:
    """
    源自tushare的数据源，
    返回值是一个Pandas的DataFrames矩阵，
    列数据需要用Keywords索引出来。

    Python之DataFrame常用方法小结
    https://blog.csdn.net/a786150017/article/details/78573055

    Pandas中DataFrame基本函数整理
    https://blog.csdn.net/brucewong0516/article/details/81782312

    https://tushare.pro/
    13524302581
    Aa12345678

    实时数据范例：
    http://qt.gtimg.cn/q=bkqtRank_A_sh,bkqtRank_A_sz
    """

    def __init__(self):
        self.token = '87e4c600d3b00362d0519ed40484fbaad3867573d61e8e8f27543a56'
        # token由https://tushare.pro/提供
        self.set_token = ts.set_token(self.token)
        self.pro = ts.pro_api()
        # print(self.pro.news(src='sina', start_date='20190326', end_date='20190327'))
        self.dailyKline = pd.DataFrame()
        self.startDate = '20170701'
        self.code = ''

        self.upperOut20 = []
        self.upper20 = []
        self.upperMid20  = []
        self.mid20 = []
        self.lowerMid20 = []
        self.lower20 = []
        self.lowerOut20 = []
        self.upper20Vol = []
        self.mid20Vol = []

        self.ma = []
        self.nList = [5, 10, 60, 144]

    def setStartDate(self, startDate):
        self.startDate = startDate

    def getList(self):
        # self.list = self.pro.query('stock_basic', exchange='', list_status='L', fields='symbol')
        # self.set_token
        temp = self.pro.query('stock_basic', exchange='', list_status='L', fields='symbol, ts_code')
        dataList = list(temp['ts_code'])
        return dataList

    def setCode(self, codeTemp):
        """
        设置代码code
        :param codeTemp:
        :return:
        """
        codeEnd = codeTemp[-3:].upper()
        # print(codeEnd)
        if len(codeTemp) == 9 and (codeEnd in ['.SZ', '.SH']):
            self.code = codeTemp
        elif len(codeTemp) == 6 and codeTemp.isnumeric():
            if codeTemp[0] == '6':
                self.code = codeTemp + '.SH'
            elif codeTemp[0] in ['0', '3']:
                self.code = codeTemp + '.SZ'
            else:
                print('代码格式错误：' + codeTemp)
                raise ValueError
        else:
            print('代码格式错误：' + codeTemp)
            raise ValueError

    def getDailyKLine(self):
        # print()
        self.dailyKline = self.pro.daily(ts_code=self.code, start_date=self.startDate,
                                         fields='ts_code, trade_date, open, high, low, close,'
                                                'pre_close, change, pct_chg, vol, amount')

    def updateDailyKLine(self):
        self._calLimit()
        self._calMa()
        self._calBoll(20, 10)
        pass

    def _calLimit(self):
        def judgeLimit(pre_close, close):
            if round(100 * (close - pre_close + 0.01) / pre_close, 2) > 10:
                return 1
            elif round(100 * (close - pre_close - 0.01) / pre_close, 2) < -10:
                return -1
            else:
                return 0

        try:
            self.dailyKline['limit'] = self.dailyKline.apply(lambda x: judgeLimit(x.pre_close, x.close), axis=1)
            self.dailyKline['limited'] = self.dailyKline.apply(lambda x: judgeLimit(x.pre_close, x.high), axis=1)
        except ValueError:
            self.dailyKline['limit'] = 0
            self.dailyKline['limited'] = 0
            # print(self.dailyKline)
            pass

    def _calBoll(self, n, nVol):
        """
        计算布林三轨
        :param n:
        :return:
        """
        '''
        valueList和valueTemp根据实际需求进行顺序和逆序，
        可以使用.reverse()
        '''
        factor = 1.026
        p1 = 1.00 / factor
        p2 = 2.00 / factor
        p3 = 2.58 / factor

        self.upperOut20.clear()
        self.upper20.clear()
        self.upperMid20.clear()
        self.mid20.clear()
        self.lowerMid20.clear()
        self.lower20.clear()
        self.lowerOut20.clear()
        self.upper20Vol.clear()
        self.mid20Vol.clear()
        valueList = list(self.dailyKline['close'])
        volList = list(self.dailyKline['vol'])
        # valueList.reverse()
        valueTemp = [float(k) for k in valueList]
        volTemp = [float(k) for k in volList]
        # boll = []
        for value in valueList:
            # boll_dict = {}
            if len(valueTemp) >= max(n, nVol):
                tempList = valueTemp[0:n]
                tempVol = volTemp[0:nVol]
                mid = numpy.mean(tempList)
                spd = numpy.std(tempList, ddof=0)
                midVol = numpy.mean(tempVol)
                spdVol = numpy.std(tempVol, ddof=0)
                upperVol = midVol + p2 * spdVol
                upperOut = mid + p3 *spd
                upper = mid + p2 * spd
                upperMid = mid + p1 * spd
                lowerMid = mid - p1 * spd
                lower = mid - p2 * spd
                lowerOut = mid - p3 * spd
                boll20_upperOut = round(upperOut, 2)
                boll20_upper = round(upper, 2)
                boll20_upperMid = round(upperMid, 2)
                boll20_mid = round(mid, 2)
                boll20_lowerMid = round(lowerMid, 2)
                boll20_lower = round(lower, 2)
                boll20_lowerOut = round(lowerOut, 2)
                boll20_upperVol = round(upperVol, 2)
                boll20_midVol = round(midVol, 2)
            else:
                boll20_upperOut = 0
                boll20_upper = 0
                boll20_upperMid = 0
                boll20_mid = 0
                boll20_lowerMid = 0
                boll20_lower = 0
                boll20_lowerOut = 0
                boll20_upperVol = 0
                boll20_midVol = 0
            # print(boll_dict)
            self.upperOut20.append(boll20_upperOut)
            self.upper20.append(boll20_upper)
            self.upperMid20.append(boll20_upperMid)
            self.mid20.append(boll20_mid)
            self.lowerMid20.append(boll20_lowerMid)
            self.lower20.append(boll20_lower)
            self.lowerOut20.append(boll20_lowerOut)
            self.upper20Vol.append(boll20_upperVol)
            self.mid20Vol.append(boll20_midVol)
            valueTemp.pop(0)
            volTemp.pop(0)

        # print(len(self.mid20))
        # print(self.mid20)
        # print(boll)
        pass
        # def average(a0, a1):
        #     return round((a0 + a1) / 2, 2)
        # print(len(self.dailyKline['close']))
        # print(len(self.mid20))
        # print(len(self.upperOut20))
        # print(len(self.mid20Vol))
        try:
            if len(self.dailyKline['close']):
                self.dailyKline['upperOut20'] = self.upperOut20
                self.dailyKline['upper20'] = self.upper20
                self.dailyKline['upperMid20'] = self.upperMid20
                self.dailyKline['mid20'] = self.mid20
                self.dailyKline['lowerMid20'] = self.lowerMid20
                self.dailyKline['lower20'] = self.lower20
                self.dailyKline['lowerOut20'] = self.lowerOut20
                # try:
                #     self.dailyKline['upperMid20'] = self.dailyKline.apply(lambda x: average(x.mid20, x.upper20), axis=1)
                #     self.dailyKline['lowerMid20'] = self.dailyKline.apply(lambda x: average(x.mid20, x.lower20), axis=1)
                # except ValueError:
                #     self.dailyKline['upperMid20'] = [round((i[0] + i[1]) / 2, 2) for i in
                #                                      zip(self.dailyKline['upper20'],
                #                                          self.dailyKline['mid20'])]
                #     self.dailyKline['lowerMid20'] = [round((i[0] + i[1]) / 2, 2) for i in
                #                                      zip(self.dailyKline['lower20'],
                #                                          self.dailyKline['mid20'])]
                bollOpenResult = []
                bollCloseResult = []
                bollMa60Result = []
                for i in range(len(self.dailyKline['open'])):
                    dailyData = self.dailyKline[i:(i + 1)]
                    dailyDict = {col: dailyData[col].tolist() for col in dailyData.columns}
                    # print('dailyData', dailyDict)
                    openList = [dailyDict['open'][0], dailyDict['upper20'][0],
                                dailyDict['upperMid20'][0], dailyDict['mid20'][0],
                                dailyDict['lowerMid20'][0], dailyDict['lower20'][0],
                                dailyDict['upperOut20'][0], dailyDict['lowerOut20'][0]]
                    closeList = [dailyDict['close'][0], dailyDict['upper20'][0],
                                 dailyDict['upperMid20'][0], dailyDict['mid20'][0],
                                 dailyDict['lowerMid20'][0], dailyDict['lower20'][0],
                                 dailyDict['upperOut20'][0], dailyDict['lowerOut20'][0]]
                    ma60List = [dailyDict['ma60'][0], dailyDict['upper20'][0],
                                 dailyDict['upperMid20'][0], dailyDict['mid20'][0],
                                 dailyDict['lowerMid20'][0], dailyDict['lower20'][0],
                                 dailyDict['upperOut20'][0], dailyDict['lowerOut20'][0]]
                    # print('OpenList', openList)
                    # print('CloseList', closeList)

                    def bollJudge(bollList):
                        if bollList[3] == 0 or bollList[0] == 0:
                            # boll is None
                            return 0
                        elif bollList[0] >= bollList[6]:
                            # upperOut
                            return 5.5
                        elif bollList[0] > bollList[1]:
                            return 5
                        elif bollList[0] == bollList[1]:
                            # upper
                            return 4
                        elif bollList[0] > bollList[2]:
                            return 3
                        elif bollList[0] == bollList[2]:
                            # upperMid
                            return 2
                        elif bollList[0] > bollList[3]:
                            return 1
                        elif bollList[0] == bollList[3]:
                            # mid20
                            return 0
                        elif bollList[0] > bollList[4]:
                            return -1
                        elif bollList[0] == bollList[4]:
                            # lowerMid
                            return -2
                        elif bollList[0] > bollList[5]:
                            return -3
                        elif bollList[0] == bollList[5]:
                            # lower
                            return -4
                        elif bollList[0] > bollList[7]:
                            return -5
                        elif bollList[0] <= bollList[7]:
                            # lowerOut
                            return -5.5
                        else:
                            return -10
                    openResult = bollJudge(openList)
                    closeResult = bollJudge(closeList)
                    ma60Result = bollJudge(ma60List)
                    # openResult = sorted(range(len(openList)), key=lambda k: openList[k])
                    # closeResult = sorted(range(len(closeList)), key=lambda k: closeList[k])
                    # print('openResult', openResult)
                    # print('closeResult', closeResult)
                    bollOpenResult.append(openResult)
                    bollCloseResult.append(closeResult)
                    bollMa60Result.append(ma60Result)
                self.dailyKline['bollPisOpen'] = bollOpenResult
                self.dailyKline['bollPisClose'] = bollCloseResult
                self.dailyKline['bollPisMa60'] = bollMa60Result
                self.dailyKline['upper20Vol'] = self.upper20Vol
                self.dailyKline['mid20Vol'] = self.mid20Vol
            else:
                self.dailyKline['upperOut20'] = 0
                self.dailyKline['upper20'] = 0
                self.dailyKline['upperMid20'] = 0
                self.dailyKline['mid20'] = 0
                self.dailyKline['lowerMid20'] = 0
                self.dailyKline['lower20'] = 0
                self.dailyKline['lowerOut20'] = 0
                self.dailyKline['bollPisOpen'] = 0
                self.dailyKline['bollPisClose'] = 0
                self.dailyKline['bollPisMa60'] = 0
                self.dailyKline['upper20Vol'] = 0
                self.dailyKline['mid20Vol'] = 0
        except KeyError or IndexError:
            self.dailyKline['upperOut20'] = 0
            self.dailyKline['upper20'] = 0
            self.dailyKline['upperMid20'] = 0
            self.dailyKline['mid20'] = 0
            self.dailyKline['lowerMid20'] = 0
            self.dailyKline['lower20'] = 0
            self.dailyKline['lowerOut20'] = 0
            self.dailyKline['bollPisOpen'] = 0
            self.dailyKline['bollPisClose'] = 0
            self.dailyKline['bollPisMa60'] = 0
            self.dailyKline['upper20Vol'] = 0
            self.dailyKline['mid20Vol'] = 0

    def _calMa(self):
        """
        计算移动平均MA
        :return:
        """
        self.ma.clear()
        valueList = list(self.dailyKline['close'])
        # valueList.reverse()
        valueTemp = [float(k) for k in valueList]
        # print(valueTemp)
        maList = []
        for i in range(len(self.nList)):
            maList.append([])
        for value in valueList:
            for i in range(len(self.nList)):
                n = self.nList[i]
                if len(valueTemp) >= n:
                    tempList = valueTemp[0:n]
                    mid = numpy.mean(tempList)
                    ma_element = round(mid, 2)
                else:
                    ma_element = 0
                maList[i].append(ma_element)
            valueTemp.pop(0)
        for i in range(len(self.nList)):
            maName = 'ma' + str(self.nList[i])
            try:
                if len(self.dailyKline['close']):
                    self.dailyKline[maName] = maList[i]
                else:
                    self.dailyKline[maName] = 0
            except KeyError or IndexError:
                self.dailyKline[maName] = 0


class DataSourceQQ:
    """
    QQ数据源，ifzq的类对象：
    https://blog.csdn.net/afgasdg/article/details/86071921
    """

    def __init__(self, code, length=1000, allLength=1000):
        """
        :param code: 无前后缀的代码
        :param length: 需要返回的数据长度
        :param allLength: 预加载的数据长度
        :return 由json转化为dict的数据
        """
        if len(code) == 6:
            if code[0] == '6':
                self.codeF = 'sh' + code
                self.codeR = code + '.sh'
            elif code[0] == '0' or code[0] == '3':
                self.codeF = 'sz' + code
                self.codeR = code + '.sz'
        else:
            raise ValueError('Invalid code:', code)
        self.length = length
        self.allLength = allLength
        self.timeLine5DaysAllinOne = None
        self.timeLine5DaysDaily = None
        self.kLineDay = None
        self.kLine60F = None

        self.upperOut20 = []
        self.upper20 = []
        self.upperMid20 = []
        self.mid20 = []
        self.lowerMid20 = []
        self.lower20 = []
        self.lowerOut20 = []
        self.upper20Vol = []
        self.mid20Vol = []
        self.ma = []
        self.nList = [60, 144]

    def updateKLine(self):
        # self._timeline()
        self._timeline5Days()
        # self._realtime('day')
        self._realtime('60')
        pass

    def _timeline(self):
        """
        获取分时数据
        :return:
        http://web.ifzq.gtimg.cn/appstock/app/minute/query?code=sh600010
        """
        host = 'http://web.ifzq.gtimg.cn/appstock/app/'
        path = 'minute/query'
        query = 'code=' + self.codeF
        url = host + path + '?' + query
        # if __name__ == '__main__':
        #     print(url)
        content = self._req(url, 0.02)

        try:
            result = []
            all_dict = json.loads(content)
            if __name__ == '__main__':
                print('_timeline', self.codeF, all_dict)
            if all_dict['code'] == 0:
                showapi_res_body = all_dict['data']
                dataList = showapi_res_body[self.codeF]
                # print(dataList)
                temp = dict()
                temp['date'] = dataList['data']['date']
                timeLine = dataList['data']['data']
                timeList = []
                for timeElement in timeLine:
                    timeArray = timeElement.split(' ')
                    # timeKeys = ('time', 'nowPrice', 'volume')
                    timeDict = {'time': timeArray[0], 'nowPrice': float(timeArray[1]), 'volume': float(timeArray[2])}
                    timeList.append(timeDict)
                temp['timeline'] = timeList
                result = temp
                self.timeLine = result
            else:
                raise ValueError
        except ValueError:
            self.timeLine = None

    def _timeline5Days(self):
        """
        获取五日分时数据
        :return:
        http://web.ifzq.gtimg.cn/appstock/app/day/query?code=sh600010
        """
        host = 'http://web.ifzq.gtimg.cn/appstock/app/'
        path = 'day/query'
        query = 'code=' + self.codeF
        url = host + path + '?' + query
        # if __name__ == '__main__':
        #     print(url)
        content = self._req(url, 0.02)
        try:
            result = []
            all_dict = json.loads(content)
            if __name__ == '__main__':
                print('_timeline5Days', self.codeF, all_dict)
            if all_dict['code'] == 0:
                showapi_res_body = all_dict['data']
                dataList = showapi_res_body[self.codeF]
                # print(dataList)

                timeListAllinOne = []
                resultDaily = []
                for dailyList in dataList['data'][::-1]:
                    # print(dailyList)
                    timeLine = dailyList['data']
                    timeListDaily = []
                    dateTemp = None
                    for timeElement in timeLine:
                        timeArray = timeElement.split(' ')
                        volumn = float(timeArray[2])
                        if dateTemp != dailyList['date']:
                            # firstVol = volumn
                            dateTemp = dailyList['date']
                            lastVol = 0
                        else:
                            pass
                        volTime = volumn - lastVol
                        lastVol = volumn
                                                # timeKeys = ('time', 'nowPrice', 'volume')

                        timeDictDaily = {'time': timeArray[0], 'nowPrice': float(timeArray[1]),
                                         'volume': float(timeArray[2]), 'volTime': volTime}
                        timeListDaily.append(timeDictDaily)
                        timeDictAllinOne = {'time': (dailyList['date'] + timeArray[0]),
                                            'nowPrice': float(timeArray[1]), 'volume': float(timeArray[2]),
                                            'volTime': volTime}
                        # timeDictAllinOne = {'date': dailyList['date'], 'time': (dailyList['date'] + timeArray[0]),
                        #                     'nowPrice': float(timeArray[1]), 'volume': float(timeArray[2])}
                        timeListAllinOne.append(timeDictAllinOne)
                    resultDaily.append({'date': dailyList['date'], 'data': timeListDaily})
                resultAllinOne = timeListAllinOne
                self.timeLine5DaysAllinOne = pd.DataFrame(resultAllinOne,
                                                          columns=['time', 'nowPrice', 'volume', 'volTime']).iloc[::-1]
                self.timeLine5DaysDaily = resultDaily
        except ValueError:
            self.timeLine5DaysAllinOne = pd.DataFrame()
            # self.timeLine5DaysAllinOne = None
            self.timeLine5DaysDaily = None

    def _realtime(self, timeType):
        """
        获取K线数据
        :param timetype:    	60 = 60分k线，
                                day = 日k线，
                                week = 周k线，
                                month = 月k线。
                                注意港股不支持5分、30分和60分k线。
        :return:
        http://web.ifzq.gtimg.cn/appstock/app/kline/mkline?param=sh600010,m60,,320
        http://web.ifzq.gtimg.cn/appstock/app/kline/kline?param=sz300100,day,,,1000
        """
        if timeType == '60':
            add_Kline = 'mKLine'
            timeValue = ',m60,,'
        elif timeType == 'day':
            add_Kline = 'KLine'
            timeValue = ',day,,,'
        elif timeType == 'week':
            add_Kline = 'KLine'
            timeValue = ',week,,,'
        elif timeType == 'month':
            add_Kline = 'KLine'
            timeValue = ',month,,,'
        elif timeType == 'minute':
            return None
        else:
            raise ValueError('Invalid timetype:', timeType)

        allLength = str(self.allLength)

        host = 'http://web.ifzq.gtimg.cn/appstock/app/kline/'
        path = add_Kline
        query = 'param=' + self.codeF + timeValue + allLength
        url = host + path + '?' + query
        # if __name__ == '__main__':
        #     print(url)
        content = self._req(url, 0.05)
        if timeType == 'day':
            try:
                result = []
                all_dict = json.loads(content)
                if __name__ == '__main__':
                    print('_realtime', self.codeF, timeType, all_dict)
                    # {'code': 0, 'msg': '', 'data': {'sh603963': {'day': [['2019-03-28', '18.500', '18.000', '19.600', '17.270', '143121.000'],
                if all_dict['code'] == 0:
                    showapi_res_body = all_dict['data']
                    dataList = showapi_res_body[self.codeF]
                    # print(dataList)
                    resultDaily = []
                    for dailyData in dataList['day'][::-1]:
                        # print(dailyData)
                        timeDictDaily = {'date': dailyData[0], 'open': float(dailyData[1]),
                                         'close': float(dailyData[2]), 'high': float(dailyData[3]),
                                         'low': float(dailyData[4]), 'volumn': float(dailyData[5])}
                        resultDaily.append(timeDictDaily)
                    self.kLineDay = pd.DataFrame(resultDaily,
                                                 columns=['time', 'open', 'close', 'high', 'low', 'volumn', 'exchange'])
                    # print(self.kLineDay)
            except ValueError:
                self.kLineDay = None
            self._calMa()
            self._calBoll(20, 10)

        elif timeType == '60':
            try:
                result = []
                all_dict = json.loads(content)
                if __name__ == '__main__':
                    print('_realtime', self.codeF, timeType, all_dict)
                if all_dict['code'] == 0:
                    showapi_res_body = all_dict['data']
                    dataList = showapi_res_body[self.codeF]['m60']
                    # print(dataList)
                    resultDaily = []
                    for dailyData in dataList[::-1]:
                        # print(dailyData)
                        timeDictDaily = {'time': dailyData[0], 'open': float(dailyData[1]),
                                         'close': float(dailyData[2]), 'high': float(dailyData[3]),
                                         'low': float(dailyData[4]), 'volumn': float(dailyData[5]),
                                         'exchange': float(dailyData[7])}
                        resultDaily.append(timeDictDaily)
                    self.kLine60F = pd.DataFrame(resultDaily,
                                                 columns=['time', 'open', 'close', 'high', 'low', 'volumn', 'exchange'])
                    # print(self.kLine60F)
            except ValueError:
                self.kLine60F = None
            self._calMa()
            self._calBoll(20, 10)

    def _req(self, url, sleepTime=0.1):
        """
        aliyun API
        :param sleepTime:
        :param url:
        :return:
        """

        url.encode('utf-8')
        if __name__ == '__main__':
            print(url)
        socket.setdefaulttimeout(10)
        content = None
        for i in range(10):
            try:
                try:
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request, timeout=10)
                    content = response.read().decode("utf-8")
                    response.close()
                    break
                except (BaseException, socket.error, OSError):
                    print('\n')
                    print(url)
                    # return ''
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionAbortedError,
                    OSError, AttributeError, KeyError, ValueError):
                time.sleep(2)
                # print('Oh,Let me have a rest! 2S!')
        if content:
            time.sleep(sleepTime)
            return content
        else:
            return ''

    def _calBoll(self, n, nVol):
        """
        计算布林三轨
        :param n:
        :return:
        """
        '''
        valueList和valueTemp根据实际需求进行顺序和逆序，
        可以使用.reverse()
        '''
        factor = 1.026
        p1 = 1.00 / factor
        p2 = 2.00 / factor
        p3 = 2.58 / factor

        self.upperOut20.clear()
        self.upper20.clear()
        self.upperMid20.clear()
        self.mid20.clear()
        self.lowerMid20.clear()
        self.lower20.clear()
        self.lowerOut20.clear()
        self.upper20Vol.clear()
        self.mid20Vol.clear()
        valueList = list(self.kLine60F['close'])
        volList = list(self.kLine60F['volumn'])
        # valueList.reverse()
        valueTemp = [float(k) for k in valueList]
        volTemp = [float(k) for k in volList]
        # boll = []
        for value in valueList:
            # boll_dict = {}
            if len(valueTemp) >= max(n, nVol):
                tempList = valueTemp[0:n]
                tempVol = volTemp[0:nVol]
                mid = numpy.mean(tempList)
                spd = numpy.std(tempList, ddof=0)
                midVol = numpy.mean(tempVol)
                spdVol = numpy.std(tempVol, ddof=0)
                upperVol = midVol + p2 * spdVol
                upperOut = mid + p3 *spd
                upper = mid + p2 * spd
                upperMid = mid + p1 * spd
                lowerMid = mid - p1 * spd
                lower = mid - p2 * spd
                lowerOut = mid - p3 * spd
                boll20_upperOut = round(upperOut, 2)
                boll20_upper = round(upper, 2)
                boll20_upperMid = round(upperMid, 2)
                boll20_mid = round(mid, 2)
                boll20_lowerMid = round(lowerMid, 2)
                boll20_lower = round(lower, 2)
                boll20_lowerOut = round(lowerOut, 2)
                boll20_upperVol = round(upperVol, 2)
                boll20_midVol = round(midVol, 2)
            else:
                boll20_upperOut = 0
                boll20_upper = 0
                boll20_upperMid = 0
                boll20_mid = 0
                boll20_lowerMid = 0
                boll20_lower = 0
                boll20_lowerOut = 0
                boll20_upperVol = 0
                boll20_midVol = 0
            # print(boll_dict)
            self.upperOut20.append(boll20_upperOut)
            self.upper20.append(boll20_upper)
            self.upperMid20.append(boll20_upperMid)
            self.mid20.append(boll20_mid)
            self.lowerMid20.append(boll20_lowerMid)
            self.lower20.append(boll20_lower)
            self.lowerOut20.append(boll20_lowerOut)
            self.upper20Vol.append(boll20_upperVol)
            self.mid20Vol.append(boll20_midVol)
            valueTemp.pop(0)
            volTemp.pop(0)

        pass
        try:
            if len(self.kLine60F['close']):
                self.kLine60F['upperOut20'] = self.upperOut20
                self.kLine60F['upper20'] = self.upper20
                self.kLine60F['upperMid20'] = self.upperMid20
                self.kLine60F['mid20'] = self.mid20
                self.kLine60F['lowerMid20'] = self.lowerMid20
                self.kLine60F['lower20'] = self.lower20
                self.kLine60F['lowerOut20'] = self.lowerOut20
                bollOpenResult = []
                bollCloseResult = []
                bollMa60Result = []
                for i in range(len(self.kLine60F['open'])):
                    min60Data = self.kLine60F[i:(i + 1)]
                    min60Dict = {col: min60Data[col].tolist() for col in min60Data.columns}
                    # print('dailyData', dailyDict)
                    openList = [min60Dict['open'][0], min60Dict['upper20'][0],
                                min60Dict['upperMid20'][0], min60Dict['mid20'][0],
                                min60Dict['lowerMid20'][0], min60Dict['lower20'][0],
                                min60Dict['upperOut20'][0], min60Dict['lowerOut20'][0]]
                    closeList = [min60Dict['close'][0], min60Dict['upper20'][0],
                                 min60Dict['upperMid20'][0], min60Dict['mid20'][0],
                                 min60Dict['lowerMid20'][0], min60Dict['lower20'][0],
                                 min60Dict['upperOut20'][0], min60Dict['lowerOut20'][0]]
                    ma60List = [min60Dict['ma60'][0], min60Dict['upper20'][0],
                                 min60Dict['upperMid20'][0], min60Dict['mid20'][0],
                                 min60Dict['lowerMid20'][0], min60Dict['lower20'][0],
                                 min60Dict['upperOut20'][0], min60Dict['lowerOut20'][0]]

                    def bollJudge(bollList):
                        if bollList[3] == 0 or bollList[0] == 0:
                            # boll is None
                            return 0
                        elif bollList[0] >= bollList[6]:
                            return 5.5
                        elif bollList[0] > bollList[1]:
                            return 5
                        elif bollList[0] == bollList[1]:
                            # upper
                            return 4
                        elif bollList[0] > bollList[2]:
                            return 3
                        elif bollList[0] == bollList[2]:
                            # upperMid
                            return 2
                        elif bollList[0] > bollList[3]:
                            return 1
                        elif bollList[0] == bollList[3]:
                            # mid20
                            return 0
                        elif bollList[0] > bollList[4]:
                            return -1
                        elif bollList[0] == bollList[4]:
                            # lowerMid
                            return -2
                        elif bollList[0] > bollList[5]:
                            return -3
                        elif bollList[0] == bollList[5]:
                            # lower
                            return -4
                        elif bollList[0] > bollList[7]:
                            return -5
                        elif bollList[0] <= bollList[7]:
                            return -5.5
                        else:
                            return -10
                    openResult = bollJudge(openList)
                    closeResult = bollJudge(closeList)
                    ma60Result = bollJudge(ma60List)

                    bollOpenResult.append(openResult)
                    bollCloseResult.append(closeResult)
                    bollMa60Result.append(ma60Result)
                self.kLine60F['bollPisOpen'] = bollOpenResult
                self.kLine60F['bollPisClose'] = bollCloseResult
                self.kLine60F['bollPisMa60'] = bollMa60Result
                self.kLine60F['upper20Vol'] = self.upper20Vol
                self.kLine60F['mid20Vol'] = self.mid20Vol
            else:
                self.kLine60F['upperOut20'] = 0
                self.kLine60F['upper20'] = 0
                self.kLine60F['upperMid20'] = 0
                self.kLine60F['mid20'] = 0
                self.kLine60F['lowerMid20'] = 0
                self.kLine60F['lower20'] = 0
                self.kLine60F['lowerOut20'] = 0
                self.kLine60F['bollPisOpen'] = 0
                self.kLine60F['bollPisClose'] = 0
                self.kLine60F['bollPisMa60'] = 0
                self.kLine60F['upper20Vol'] = 0
                self.kLine60F['mid20Vol'] = 0
        except KeyError or IndexError:
            self.kLine60F['upperOut20'] = 0
            self.kLine60F['upper20'] = 0
            self.kLine60F['upperMid20'] = 0
            self.kLine60F['mid20'] = 0
            self.kLine60F['lowerMid20'] = 0
            self.kLine60F['lower20'] = 0
            self.kLine60F['lowerOut20'] = 0
            self.kLine60F['bollPisOpen'] = 0
            self.kLine60F['bollPisClose'] = 0
            self.kLine60F['bollPisMa60'] = 0
            self.kLine60F['upper20Vol'] = 0
            self.kLine60F['mid20Vol'] = 0

    def _calMa(self):
        """
        计算移动平均MA
        :return:
        """
        self.ma.clear()
        valueList = list(self.kLine60F['close'])
        # valueList.reverse()
        valueTemp = [float(k) for k in valueList]
        # print(valueTemp)
        maList = []
        for i in range(len(self.nList)):
            maList.append([])
        for value in valueList:
            for i in range(len(self.nList)):
                n = self.nList[i]
                if len(valueTemp) >= n:
                    tempList = valueTemp[0:n]
                    mid = numpy.mean(tempList)
                    ma_element = round(mid, 2)
                else:
                    ma_element = 0
                maList[i].append(ma_element)
            valueTemp.pop(0)
        for i in range(len(self.nList)):
            maName = 'ma' + str(self.nList[i])
            try:
                if len(self.kLine60F['close']):
                    self.kLine60F[maName] = maList[i]
                else:
                    self.kLine60F[maName] = 0
            except KeyError or IndexError:
                self.kLine60F[maName] = 0


if __name__ == '__main__':
    debug = 0
    code = '603963'
    # a = code.partition('.')
    # code = a[0]
    # print(a)
    data = DataTuShare()
    stockList = data.getList()
    print(stockList)
    if not debug:
        data.setCode(code)
        data.getDailyKLine()
        # print(data.dailyKline)
        data.updateDailyKLine()
        # print(data.dailyKline)
        while True:
            try:
                data.dailyKline.to_csv('d:/' + code + '.csv')
                break
            except PermissionError:
                input('The file is open...please close it!!!')
    if debug:
        j = 0
        for code in stockList:
            data.setCode(code)
            # print(code)
            while True:
                # noinspection PyBroadException
                try:
                    data.getDailyKLine()
                    # data.updateDailyKLine()
                    break
                except Exception:
                    print(code, 'time sleep...')
                    time.sleep(60)
            data.updateDailyKLine()
            try:
                if len(data.dailyKline['close']):
                    print(code, 'mid20:\t', data.dailyKline['mid20'][0], '\trunning...')
                else:
                    print(code, 'no data!!!')
            except ValueError or KeyError or IndexError:
                pass
            try:
                if data.dailyKline.head(1)['limit'][0] == 1:
                    # {col: data.dailyKline[col].tolist() for col in data.dailyKline.columns}
                    print(dict(data.dailyKline[0:1]['ts_code'])[0], 'Limited!!!')
                    j += 1
            except:
                pass
        print(j)

    if code is not None:
        test = DataSourceQQ(code)
        test.updateKLine()
        # test = DataSource_iFeng(code)
        pass
    else:
        raise ValueError
    print(test.timeLine5DaysAllinOne)
    test.timeLine5DaysAllinOne.to_csv('D:/min.csv')
    b = test.kLine60F
    b.to_csv('D:/hour.csv')
    print(b)
    # print(test.timeLine)
    # for i in test.timeLine5DaysAllinOne:
    #     print(i)
    # for i in test.timeLine5DaysDaily:
    #     print(i)
    # for i in test.kLine60F:
    #     print(i)
    # print(test.kLineDay['record'])
