import urllib.request
import urllib.error
import socket
import time
import json
import numpy
import tushare as ts
import pandas as pd
import pymysql
import sqlalchemy

from sqlalchemy import create_engine
from Dino.DataSource.MySQL import MySQL

"""
http://api.finance.ifeng.com/akdaily/?code=sh600030&type=last
[
      "2018-10-31 11:00:00", # 日期
      "3146.23", # 开盘价
      "3146.23", # 最高价
      "3130.41", # 收盘价
      "3130.21", # 最低价
      107709,    # 成交量
      "-15.82",  # 价格变动
      -0.5,      # 涨跌幅
      "3130.04", # 5日均价
      "3119.8",  # 10日均价
      "3109.55", # 20日均价
      159535,    # 5日均量
      150064,    # 10日均量
      138100,    # 20日均量
      0          # 换手率[注：指数无此项]
    ],
"""
"""
http://api.finance.ifeng.com/akmin?scode=sh000300&type=60
[
      "2018-10-31", # 日期
      "3146.23", # 开盘价
      "3146.23", # 最高价
      "3130.41", # 收盘价
      "3130.21", # 最低价
      107709,    # 成交量
      "-15.82",  # 价格变动
      -0.5,      # 涨跌幅
      "3130.04", # 5日均价
      "3119.8",  # 10日均价
      "3109.55", # 20日均价
      159535,    # 5日均量
      150064,    # 10日均量
      138100,    # 20日均量
    ],
"""

def judgeLimit(pre_close, close):
    if round(100 * (close - pre_close + 0.01) / pre_close, 2) > 10:
        return 1
    elif round(100 * (close - pre_close - 0.01) / pre_close, 2) < -10:
        return -1
    else:
        return 0

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
        return numpy.nan

def trendJudgeMA(m):
    if m > 0.01:
        return 1
    elif m < -0.01:
        return -1
    else:
        return 0

def trendJudgeWidth(m):
    if m > 1:
        return 1
    elif m < -1:
        return -1
    else:
        return 0

def dateTransfer(dateIn):
    a = time.strptime(dateIn, '%Y-%m-%d')
    dateOut = time.strftime('%Y%m%d', a)
    return dateOut


class DataSourceQQ:
    """
    整个常用数据源的类对象：
    :param code:无前后缀的代码
    :param length:需要返回的数据长度
    :param allLength:预加载的数据长度
    :return 由json转化为dict的数据

    """
    def __init__(self, code, length = 1000, allLength = 1000):
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
        self._timeline()
        self._timeline5Days()
        self.kLineDay = self._realtime('day')
        self.kLine60F = self._realtime('60')


    def _timeline(self):
        """
        获取分时数据
        :param code:
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
                print(all_dict)
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
                    timeDict = {'time': timeArray[0], 'nowPrice': timeArray[1], 'volume': timeArray[2]}
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
        :param code:
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
                print(all_dict)
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
                    for timeElement in timeLine:
                        timeArray = timeElement.split(' ')
                        # timeKeys = ('time', 'nowPrice', 'volume')
                        timeDictDaily = {'time': timeArray[0], 'nowPrice': timeArray[1], 'volume': timeArray[2]}
                        timeListDaily.append(timeDictDaily)

                        timeDictAllinOne = {'date':dailyList['date'], 'time': timeArray[0], 'nowPrice': timeArray[1], 'volume': timeArray[2]}
                        timeListAllinOne.append(timeDictAllinOne)
                    resultDaily.append({'date':dailyList['date'], 'data':timeListDaily})
                resultAllinOne = timeListAllinOne
                self.timeLine5DaysAllinOne = resultAllinOne
                self.timeLine5DaysDaily = resultDaily
        except ValueError:
            self.timeLine5DaysAllinOne = None
            self.timeLine5DaysDaily = None


    def _realtime(self, timeType):
        """
        获取K线数据
        :param allLength:
        :param code:
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
        content = json.loads(self._req(url, 0.05))
        return content


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


class DataTuShareMul:
    def __init__(self):
        self.token = '6910bc790677ae86aa121ed1747c14cf91d06a509be70dc72de0019f'
        # token由https://tushare.pro/提供
        self.set_token = ts.set_token(self.token)
        self.pro = ts.pro_api()
        self.startDate = '20170101'
        self.connection = create_engine('mysql+pymysql://root:star2249@localhost:3306/stocks?charset=utf8')
        self.nList = [5, 10, 60, 144]
        self.colList = None
        self.stocks_config = \
            {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'star2249',
            'db': 'stocks',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
            }
        self.sDB = MySQL(self.stocks_config)
        self._get_DateTime()

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setCode(self, codeTemp):
        """
        设置代码code
        :param codeTemp:
        :return:
        """
        codeEnd = codeTemp[-3:].upper()
        # print(codeEnd)
        if len(codeTemp) == 9 and (codeEnd in ['.SZ', '.SH']):
            code = codeTemp
        elif len(codeTemp) == 6 and codeTemp.isnumeric():
            if codeTemp[0] == '6':
                code = codeTemp + '.SH'
            elif codeTemp[0] in ['0', '3']:
                code = codeTemp + '.SZ'
            else:
                print('代码格式错误：' + codeTemp)
                raise ValueError
        else:
            print('代码格式错误：' + codeTemp)
            raise ValueError
        return code

    def _getDailyKLine(self, code=None):
        """
        获取日线数据
        针对start_date需要优化，判断数据库的max(trade_date)
        :return:
        """
        # print()
        if code:
            dailyKline = self.pro.daily(ts_code=code, start_date=self.startDate,
                                         fields='ts_code, trade_date, open, high, low, close,'
                                                'pre_close, change, pct_chg, vol, amount')
        else:
            dailyKline = None
        return dailyKline

    def updateDailyKLine(self, colList, code=None):
        """
        更新各项指标，若数据库存在，则直接加载数据库。
        针对start_date需要优化，判断数据库的max(trade_date)
        :return:
        """
        # if code:
        #     tableName = code.replace('.', '').lower()
        #     sql = 'select max(trade_date) from ' + tableName + ";"
        #     maxTradeDate = None
        #     try:
        #         self.sDB.execSQL(sql)
        #         maxTradeDate = self.sDB.dbReturn[0]['max(trade_date)']
        #         self.sDB.close()
        #     # except pymysql.err or ConnectionRefusedError:
        #     except:
        #         pass
        #     if maxTradeDate and maxTradeDate == self.dateTime['shortDate']:
        #         dailyKline = self._loadDailyKLine(tableName)
        #     else:
        #         dailyKline = self._getDailyKLine(code)
        #         dailyKline = self._calLimit(dailyKline)
        #         dailyKline = self._calMa(dailyKline)
        #         dailyKline = self._calBoll(dailyKline, 20, 10)
        #         if (not dailyKline.empty) and (not colList):
        #             colList = list(dailyKline.columns)
        #             for i in ['ts_code', 'trade_date']:
        #                 try:
        #                     colList.remove(i)
        #                 except ValueError:
        #                     pass
        #         # print(self.colList)
        #         '''
        #         为calPosition计算表头列表
        #         '''
        #         dailyKline = self._calPosition(dailyKline, colList)
        #         self._saveDailyKLine(tableName, dailyKline)
        if code:
            tableName = code.replace('.', '').lower()
            dailyKline = self._getDailyKLine(code)
            dailyKline = self._calLimit(dailyKline)
            dailyKline = self._calMa(dailyKline)
            dailyKline = self._calBoll(dailyKline, 20, 10)
            if (not dailyKline.empty) and (not colList):
                colList = list(dailyKline.columns)
                for i in ['ts_code', 'trade_date']:
                    try:
                        colList.remove(i)
                    except ValueError:
                        pass
            '''
            为calPosition计算表头列表
            '''
            dailyKline = self._calPosition(dailyKline, colList)
            dailyKline.to_csv('d:/' + tableName + '.csv')

        return dailyKline

    def _saveDailyKLine(self, tableName, dailyKline):
        sql = "drop table if exists " + tableName + ";"
        try:
            self.sDB.execSQL(sql)
            self.sDB.close()
        # except UserWarning:
        except:
            pass
        try:
            dailyKline.to_sql(tableName, self.connection, if_exists='replace', index=False)
        except sqlalchemy.exc.OperationalError:
            pass

    def _loadDailyKLine(self, tableName):
        dailyKline = pd.read_sql_table(tableName, self.connection)
        return dailyKline

    def _calLimit(self, dailyKlineIn):
        dailyKlineOut = dailyKlineIn
        try:
            dailyKlineOut['limit'] = dailyKlineIn.apply(lambda x: judgeLimit(x.pre_close, x.close), axis=1)
            dailyKlineOut['limited'] = dailyKlineIn.apply(lambda x: judgeLimit(x.pre_close, x.high), axis=1)
        except ValueError:
            dailyKlineOut['limit'] = 0
            dailyKlineOut['limited'] = 0
            # print(self.dailyKline)
        return dailyKlineOut

    def _calBoll(self, dailyKlineIn, n, nVol):
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

        dailyKlineOut = dailyKlineIn

        upperOut20 = []
        upper20 = []
        upperMid20 = []
        mid20 = []
        lowerMid20 = []
        lower20 = []
        lowerOut20 = []
        upper20Vol = []
        mid20Vol = []
        width20 = []
        valueList = list(dailyKlineIn['close'])
        volList = list(dailyKlineIn['vol'])
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
                width = 100 * (boll20_upper - boll20_lower) / boll20_mid
                boll20_width = round(width, 2)
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
                boll20_width = 0
                boll20_upperVol = 0
                boll20_midVol = 0
            upperOut20.append(boll20_upperOut)
            upper20.append(boll20_upper)
            upperMid20.append(boll20_upperMid)
            mid20.append(boll20_mid)
            lowerMid20.append(boll20_lowerMid)
            lower20.append(boll20_lower)
            lowerOut20.append(boll20_lowerOut)
            width20.append(boll20_width)
            upper20Vol.append(boll20_upperVol)
            mid20Vol.append(boll20_midVol)
            valueTemp.pop(0)
            volTemp.pop(0)
        pass
        try:
            if len(dailyKlineIn['close']):
                dailyKlineOut['upperOut20'] = upperOut20
                dailyKlineOut['upper20'] = upper20
                dailyKlineOut['upperMid20'] = upperMid20
                dailyKlineOut['mid20'] = mid20
                dailyKlineOut['lowerMid20'] = lowerMid20
                dailyKlineOut['lower20'] = lower20
                dailyKlineOut['lowerOut20'] = lowerOut20
                dailyKlineOut['width20'] = width20
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
                for i in range(len(dailyKlineIn['open'])):
                    dailyData = dailyKlineIn[i:(i + 1)]
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
                dailyKlineOut['bollPisOpen'] = bollOpenResult
                dailyKlineOut['bollPisClose'] = bollCloseResult
                dailyKlineOut['bollPisMa60'] = bollMa60Result
                dailyKlineOut['upper20Vol'] = upper20Vol
                dailyKlineOut['mid20Vol'] = mid20Vol
            else:
                dailyKlineOut['upperOut20'] = 0
                dailyKlineOut['upper20'] = 0
                dailyKlineOut['upperMid20'] = 0
                dailyKlineOut['mid20'] = 0
                dailyKlineOut['lowerMid20'] = 0
                dailyKlineOut['lower20'] = 0
                dailyKlineOut['lowerOut20'] = 0
                dailyKlineOut['width20'] = 0
                dailyKlineOut['bollPisOpen'] = 0
                dailyKlineOut['bollPisClose'] = 0
                dailyKlineOut['bollPisMa60'] = 0
                dailyKlineOut['upper20Vol'] = 0
                dailyKlineOut['mid20Vol'] = 0
        except KeyError or IndexError:
            dailyKlineOut['upperOut20'] = 0
            dailyKlineOut['upper20'] = 0
            dailyKlineOut['upperMid20'] = 0
            dailyKlineOut['mid20'] = 0
            dailyKlineOut['lowerMid20'] = 0
            dailyKlineOut['lower20'] = 0
            dailyKlineOut['lowerOut20'] = 0
            dailyKlineOut['width20'] = 0
            dailyKlineOut['bollPisOpen'] = 0
            dailyKlineOut['bollPisClose'] = 0
            dailyKlineOut['bollPisMa60'] = 0
            dailyKlineOut['upper20Vol'] = 0
            dailyKlineOut['mid20Vol'] = 0
        return dailyKlineOut

    def _calMa(self, dailyKlineIn):
        """
        计算移动平均MA
        :return:
        """
        dailyKlineOut = dailyKlineIn
        valueList = list(dailyKlineIn['close'])
        valueTemp = [float(k) for k in valueList]
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
                if len(dailyKlineIn['close']):
                    dailyKlineOut[maName] = maList[i]
                else:
                    dailyKlineOut[maName] = 0
            except KeyError or IndexError:
                dailyKlineOut[maName] = 0
        return dailyKlineOut

    def _calPosition(self, dailyKlineIn, colList):
        """
        针对mid20、width20、ma60、ma144的趋势进行量化分析（平/升/降，开口/收口/走平）
        :return:
        """
        dailyKlineOut = dailyKlineIn
        frame_1 = dailyKlineIn[:-1].reset_index()[colList]
        frame_2 = dailyKlineIn[1:].reset_index()[colList]
        result = (frame_1 - frame_2)
        # result.to_csv('D:/diff.csv')
        dailyKlineOut['upper20tr'] = result.apply(lambda x: trendJudgeMA(x.upper20), axis=1)
        dailyKlineOut['mid20tr'] = result.apply(lambda x: trendJudgeMA(x.mid20), axis=1)
        dailyKlineOut['lower20tr'] = result.apply(lambda x: trendJudgeMA(x.lower20), axis=1)
        dailyKlineOut['width20tr'] = result.apply(lambda x: trendJudgeWidth(x.width20), axis=1)
        dailyKlineOut['ma60tr'] = result.apply(lambda x: trendJudgeMA(x.ma60), axis=1)
        dailyKlineOut['ma144tr'] = result.apply(lambda x: trendJudgeMA(x.ma144), axis=1)
        return dailyKlineOut

    def _get_DateTime(self):
        """
        获取当前日期和时间
        :return:
        """
        timeStamp = time.localtime()
        # DateTime = {}
        fullDate = (time.strftime("%Y-%m-%d", timeStamp))
        shortDate = (time.strftime("%Y%m%d", timeStamp))
        fullTime = (time.strftime("%H:%M:%S", timeStamp))
        shortTime = (time.strftime("%H%M%S", timeStamp))
        keys = ['fullDate', 'shortDate', 'fullTime', 'shortTime']
        # print(keys)
        values = [fullDate, shortDate, fullTime, shortTime]
        # print(values)
        self.dateTime = dict(zip(keys, values))



class DataSource_iFeng:
    """
    整个常用数据源的类对象：
    :param code:无前后缀的代码
    :param length:需要返回的数据长度
    :param allLength:预加载的数据长度
    :return 由json转化为dict的数据

    """
    def __init__(self, code, length = 1000, allLength = 1000):
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
        self.kLineDay = self._realtime('day')
        self.kLine60F = self._realtime('60')


    def _realtime(self, timeType):
        """
        获取K线数据
        :param allLength:
        :param code:
        :param timetype:    	60 = 60分k线，
                                day = 日k线，
                                week = 周k线，
                                month = 月k线。
                                注意港股不支持5分、30分和60分k线。
        :return:
        http://api.finance.ifeng.com/akdaily?code=sh600030&type=last
        http://api.finance.ifeng.com/akmin?scode=sh000300&type=60
        """
        if timeType == '60':
            add_Kline = 'min?s'
            timeValue = '60'
        elif timeType == 'day':
            add_Kline = 'daily?'
            timeValue = 'last'
        else:
            raise ValueError('Invalid timetype:', timeType)

        host = 'http://api.finance.ifeng.com/ak'
        path = add_Kline
        query = 'code=' + self.codeF + '&type=' + timeValue
        url = host + path + query
        if __name__ == '__main__':
            print(url)
        content = json.loads(self._req(url, 0.05))
        return content


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

