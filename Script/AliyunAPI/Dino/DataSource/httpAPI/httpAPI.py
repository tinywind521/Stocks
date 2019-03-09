import urllib.request
import urllib.error
import socket
import time
import json


class DataSource:
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
        self.timeLine = self.__timeline()
        self.timeLine5Days = self.__timeline5Days()
        self.kLineDay = self.__realtime('day')
        self.kLine60F = self.__realtime('60')


    def __timeline(self):
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
        # print(url)

        content = json.load(self.__req(url, 0.02))
        return content


    def __timeline5Days(self):
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
        # print(url)

        content = json.load(self.__req(url, 0.02))
        return content


    def __realtime(self, timeType):
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
        # if len(code) == 6:
        #     if code[0] == '6':
        #         code = 'sh' + code
        #     elif code[0] == '0' or code[0] == '3':
        #         code = 'sz' + code
        # elif len(code) == 8:
        #     code = code
        # else:
        #     raise ValueError('Invalid code:', code)

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
        query = 'param=' + code + timeValue + allLength
        url = host + path + '?' + query

        content = json.load(self.__req(url, 0.05))
        return content


    def __req(self, url, sleepTime=0.1):
        """
        aliyun API
        :param sleepTime:
        :param url:
        :return:
        """

        url.encode('utf-8')
        # print(url)
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
    code = input('Please input the code(600001): ')
    test = DataSource(code)
    print(test.timeLine)
    print(test.timeLine5Days)
