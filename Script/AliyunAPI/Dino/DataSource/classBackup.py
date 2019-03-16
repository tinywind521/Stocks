import urllib.request
import urllib.error
import socket
import time
import json

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

