#   import urllib.request
#   import sys
#   import ssl

from aliyun import aliyun_request
from functions import function, getValue


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

    content = aliyun_request.req(url, appcode)
    return content


def realtime(code, beginday, timetype, qtype='bfq', appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取K线数据
    :param code:
    :param beginday:
    :param timetype:    	5 = 5分k线(默认) ，
                            30 = 30分k线，
                            60 = 60分k线，
                            day = 日k线，
                            week = 周k线，
                            month = 月k线。
                            注意港股不支持5分、30分和60分k线。
    :param qtype:
    :param appcode:
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/realtime-k'
    method = 'GET'
    querys = 'beginDay=' + beginday + '&code=' + code + '&time=' + timetype + '&type=' + qtype
    bodys = {}
    url = host + path + '?' + querys

    content = aliyun_request.req(url, appcode)
    return content


def mainindex(code, beginday, timetype, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取大盘K线数据
    :param code:
    :param beginday:
    :param timetype:
    :param appcode:
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/index-kline'
    method = 'GET'
#   appcode = '你自己的AppCode'
    querys = 'beginDay=' + beginday + '&code=' + code + '&time=' + timetype
    bodys = {}
    url = host + path + '?' + querys

    content = aliyun_request.req(url, appcode)
    return content


def stocklist(market, currentPage, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取指定页数的代码
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/stocklist'
    method = 'GET'
    # appcode = '你自己的AppCode'
    # currentPage = 1
    querys = 'market=' + market + '&page=' + format(currentPage, 'd')
    bodys = {}
    url = host + path + '?' + querys

    content = aliyun_request.req(url, appcode)
    return content


def daily_ssd(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    读取每日非正常列表
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/stop-start-divide'
    method = 'GET'
    # appcode = '你自己的AppCode'
    date = getValue.get_DateTime()['shortdate']
    querys = 'date=' + date
    bodys = {}
    url = host + path + '?' + querys

    content = aliyun_request.req(url, appcode)
    return content


def block_list(appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取板块列表
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/stock-block-list'
    method = 'GET'
    # appcode = '你自己的AppCode'
    querys = ''
    bodys = {}
    url = host + path

    content = aliyun_request.req(url, appcode)
    return content


def block_stocks(blockId, currentPage, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    获取板块内指定页数的个股
    :param blockId:
    :param currentPage:
    :param appcode:
    :return:
    """
    host = 'https://ali-stock.showapi.com'
    path = '/stock-in-block'
    method = 'GET'
    # appcode = '你自己的AppCode'
    querys = 'page=' + format(currentPage, 'd') + '&typeId=' + blockId
    bodys = {}
    url = host + path + '?' + querys

    content = aliyun_request.req(url, appcode)
    return content
