#   import urllib.request
#   import sys
#   import ssl
#
# from functions import function, getValue
from http_api import qtimq_request
from http_api import aliyun_request


def timeline(code, day, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取分时数据
    :param code:
    :param day:
    :param appcode:
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/timeline'
    method = 'GET'
    #   appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
    #   querys = 'code=000000&day=1'
    bodys = {}
    #   url = host + path + '?' + querys
    url = host + path + '?' + "code=" + code + '&' + "day=" + day
    # print(url)

    content = aliyun_request.req(url, appcode)
    return content


def realtime(code, allLength, timetype):
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

    if timetype == '60':
        add_Kline = 'mkline'
        timeValue = ',m60,,'
    elif timetype == 'day':
        add_Kline = 'kline'
        timeValue = ',day,,,'
    elif timetype == 'week':
        add_Kline = 'kline'
        timeValue = ',week,,,'
    elif timetype == 'month':
        add_Kline = 'kline'
        timeValue = ',month,,,'
    else:
        raise ValueError('Invalid timetype:', timetype)

    allLength = str(allLength)

    host = 'http://web.ifzq.gtimg.cn/appstock/app/kline/'
    path = add_Kline
    querys = 'param=' + code + timeValue + allLength
    url = host + path + '?' + querys

    content = qtimq_request.req(url, 0.05)
    return content
