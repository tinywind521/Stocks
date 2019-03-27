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
    """
    def __init__(self):
        self.token = '220faa2050cc97b5ad1ff92c000535c01e5ab6c792cbd63addbe7ff1'
        # token由https://tushare.pro/提供
        self.set_token = ts.set_token(self.token)
        self.pro = ts.pro_api()
        self.dailyKline = pd.DataFrame()
        self.startDate = '20180101'
        self.code = ''
        self.mid20 = []
        self.upper20 = []
        self.lower20 = []

    def setStartDate(self, startDate):
        self.startDate = startDate

    def getList(self):
        # self.list = self.pro.query('stock_basic', exchange='', list_status='L', fields='symbol')
        # self.set_token
        temp = self.pro.query('stock_basic', exchange='', list_status='L', fields='symbol, ts_code')
        dataList = list(temp['ts_code'])
        return dataList

    def setCode(self, codeTemp):
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
        self.dailyKline = self.pro.daily(ts_code = self.code, start_date = self.startDate,
                                         fields = 'ts_code,trade_date, open, high, low, close,'
                                                'pre_close, change, pct_chg, vol, amount')

    def updateDailyKLine(self):
        self._calLimit()
        self._calBoll(20, 2)
        pass

    def _calLimit(self):
        def judgeLimit(pre_close, close):
            if round(100*(close - pre_close + 0.01) / pre_close, 2) > 10:
                return 1
            elif round(100*(close - pre_close - 0.01) / pre_close, 2) < -10:
                return -1
            else:
                return 0
        try:
            self.dailyKline['limit'] = self.dailyKline.apply(lambda x: judgeLimit(x.pre_close, x.close), axis=1)
        except ValueError:
            self.dailyKline['limit'] = 0
            # print(self.dailyKline)
            pass

    def _calBoll(self, n, p):
        """
        计算布林三轨
        :param n:
        :param p:
        :return:
        """
        '''
        valueList和valueTemp根据实际需求进行顺序和逆序，
        可以使用.reverse()
        '''
        self.mid20.clear()
        self.upper20.clear()
        self.lower20.clear()
        valueList = list(self.dailyKline['close'])
        # valueList.reverse()
        valueTemp = [float(k) for k in valueList]
        # print(valueTemp)
        # boll = []
        for value in valueList:
            # boll_dict = {}
            if len(valueTemp) >= n:
                tempList = valueTemp[0:n]
                mid = numpy.mean(tempList)
                spd = numpy.std(tempList, ddof=0)
                upper = mid + p * spd
                lower = mid - p * spd
                boll20_mid = round(mid, 2)
                boll20_upper = round(upper, 2)
                boll20_lower = round(lower, 2)
                # boll_dict['mid'] = round(mid, 2)
                # boll_dict['upper'] = round(upper, 2)
                # boll_dict['lower'] = round(lower, 2)
            else:
                boll20_mid = 0
                boll20_upper = 0
                boll20_lower = 0
                # boll_dict['mid'] = 0
                # boll_dict['upper'] = 0
                # boll_dict['lower'] = 0
            # print(boll_dict)
            self.mid20.append(boll20_mid)
            self.upper20.append(boll20_upper)
            self.lower20.append(boll20_lower)
            valueTemp.pop(0)
        # print(len(self.mid20))
        # print(self.mid20)
        # print(boll)
        def average(a0, a1):
            return round((a0 + a1)/2, 2)
        self.dailyKline['upper20'] = self.upper20
        self.dailyKline['mid20'] = self.mid20
        self.dailyKline['lower20'] = self.lower20
        self.dailyKline['upperMid20'] = self.dailyKline.apply(lambda x: average(x.mid20, x.upper20), axis=1)
        self.dailyKline['lowerMid20'] = self.dailyKline.apply(lambda x: average(x.mid20, x.lower20), axis=1)


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
        #self.kLineDay = self._realtime('day')
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


if __name__ == '__main__':
    debug = 1
    code = '000001.sz'
    a = code.partition('.')
    code = a[0]
    # print(a)
    data = DataTuShare()
    stockList = data.getList()
    print(stockList)
    if not debug:
        data.setCode(code)
        data.getDailyKLine()
        # print(data.dailyKline)
        data.updateDailyKLine()
        print(data.dailyKline)
    if debug:
        j = 0
        for code in stockList:
            data.setCode(code)
            # print(code)
            while True:
                try:
                    data.getDailyKLine()
                    data.updateDailyKLine()
                    break
                except Exception:
                    print(code, 'time sleep...')
                    time.sleep(60)
            data.updateDailyKLine()
            print(code, 'mid20:', data.dailyKline['mid20'][0], '\trunning...')
            try:
                if data.dailyKline.head(1)['limit'][0] == 1:
                    # {col: data.dailyKline[col].tolist() for col in data.dailyKline.columns}
                    print(dict(data.dailyKline[0:1]['ts_code'])[0], 'Limited!!!')
                    j += 1
            except:
                pass
        print(j)


    # if code != None:
    #     test = DataSourceQQ(code)
    #     # test = DataSource_iFeng(code)
    #     pass
    # else:
    #     raise ValueError
    # print(test.timeLine)
    # for i in test.timeLine5DaysAllinOne:
    #     print(i)
    # print()
    # for i in test.timeLine5DaysDaily:
    #     print(i)
    # print(test.kLine60F['record'])
    # for i in test.kLine60F['record']:
    #     print(i)
    # # print(test.kLineDay['record'])
    # for i in test.kLineDay['record']:
    #     print(i)
