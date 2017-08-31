#   import urllib.request
#   import sys
#   import ssl
#
# from functions import function, getValue
from http_api import qtimq_request


def timeline(code):
    """
    获取分时数据
    :param code:
    :return:

    http://web.ifzq.gtimg.cn/appstock/app/minute/query?code=sh600010
    """
    host = 'http://web.ifzq.gtimg.cn/appstock/app/'
    path = 'minute/query'
    querys = 'code=' + code
    url = host + path + '?' + querys
    # print(url)

    content = qtimq_request.req(url, 0.05)
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
