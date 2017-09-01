import urllib.request
import urllib.error
import urllib.parse
import socket
import time
import requests
import time


def hkex():
    """
    获取hkex数据。
    :return:
    """
    # a = date
    host = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t='
    # Referer = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t='
    # path = '/timeline'
    method = 'GET'
    # bodys = {
    #         'source': 'Ths_iwencai_Xuangu',
    #         'question': '股票代码,股票简称,涨跌幅,开盘价不复权,最高价不复权,最低价不复权,收盘价不复权,开盘价前复权,最高价前复权,最低价前复权,收盘价前复权,成交量(股),换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值',
    #         'kefu_user_id': '3369015226052771840',
    #         'kefu_record_id': '503b2760-4619-48ce-b502-ac5daf578fc5',
    #         'user_id': '',
    #         'log_info': '{"other_info":"{\"eventId\":\"iwencai_app_send_click\",\"ct\":1504256639535}","other_utype":"random","other_uid":"1322605817"}',
    #         'user_name': '7133885344',
    #         '_': '1504256639538',
    #         }
    bodys = {
            'token':'3ecda4f71d9daa85e5b040da069791dd',
            'p':'0',
            'perpage':'100',
            }

    # url = host
    url = 'http://www.iwencai.com/stockpick/cache?token=3ecda4f71d9daa85e5b040da069791dd&p=0&perpage=100'
    # url = 'http://www.iwencai.com/stockpick/load-data?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E8%82%A1%E7%A5%A8%E4%BB%A3%E7%A0%81%2C%E8%82%A1%E7%A5%A8%E7%AE%80%E7%A7%B0%2C%E6%B6%A8%E8%B7%8C%E5%B9%85%2C%E5%BC%80%E7%9B%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E9%AB%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E4%BD%8E%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%94%B6%E7%9B%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E5%BC%80%E7%9B%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E9%AB%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E4%BD%8E%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%94%B6%E7%9B%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%88%90%E4%BA%A4%E9%87%8F(%E8%82%A1)%2C%E6%8D%A2%E6%89%8B%E7%8E%87(%25)%2C%E6%8C%AF%E5%B9%85%2C%E4%B8%8A%E5%B8%82%E4%B8%8D%E8%B6%85%E8%BF%87%EF%BC%8C%E4%B8%8A%E5%B8%82%E5%A4%A9%E6%95%B0%2C%E6%8A%80%E6%9C%AF%E5%BD%A2%E6%80%81%2CA%E8%82%A1%E6%B5%81%E9%80%9A%E5%B8%82%E5%80%BC&queryarea='
    Referer = 'http://www.iwencai.com/data-robot/extract-new?query=%E8%82%A1%E7%A5%A8%E4%BB%A3%E7%A0%81%2C%E8%82%A1%E7%A5%A8%E7%AE%80%E7%A7%B0%2C%E6%B6%A8%E8%B7%8C%E5%B9%85%2C%E5%BC%80%E7%9B%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E9%AB%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E4%BD%8E%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%94%B6%E7%9B%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E5%BC%80%E7%9B%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E9%AB%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E4%BD%8E%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%94%B6%E7%9B%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%88%90%E4%BA%A4%E9%87%8F(%E8%82%A1)%2C%E6%8D%A2%E6%89%8B%E7%8E%87(%25)%2C%E6%8C%AF%E5%B9%85%2C%E4%B8%8A%E5%B8%82%E4%B8%8D%E8%B6%85%E8%BF%87%EF%BC%8C%E4%B8%8A%E5%B8%82%E5%A4%A9%E6%95%B0%2C%E6%8A%80%E6%9C%AF%E5%BD%A2%E6%80%81%2CA%E8%82%A1%E6%B5%81%E9%80%9A%E5%B8%82%E5%80%BC&firstDraw=1'

    content = req(url, bodys, Referer)
    # time.sleep(1)
    return content



def req(url, data, referer=None, **headers):
    """

    :param url:
    :param data:
    :param referer:
    :param headers:
    :return:
    """
    while True:
        try:
            request = urllib.request.Request(url)
            request.add_header('Connection',
                               'keep-alive')
            while True:
                try:
                    response = urllib.request.urlopen(request, timeout=5)
                    response.close()
                    responseHeader = dict(response.info().items())
                    cookie = responseHeader['Set-Cookie']
                    print(cookie)
                    # response.close()
                    break
                except socket.timeout or urllib.error:
                    pass
            # time.sleep(0.1)
            # print(cookie)

            request.add_header('Host',
                               'www.iwencai.com')
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/59.0.3071.115 Safari/537.36')
            request.add_header('Accept',
                               'application/json, text/javascript, */*; q=0.01')
            request.add_header('Accept-Encoding',
                               'gzip, deflate')
            request.add_header('Accept-Language',
                               'zh-CN,zh;q=0.8')
            request.add_header('Connection',
                               'keep-alive')
            request.add_header('Cookie',
                               (cookie.split(';'))[0])
            request.add_header('X-Requested-With',
                               'XMLHttpRequest')
            request.add_header('Upgrade-Insecure-Requests',
                               '1')

            if referer:
                request.add_header('Referer', referer)
            if headers:
                for k in headers.keys():
                    request.add_header(k, headers[k])
            s = ''
            for element in data:
                s += element + '=' + data[element] + '&'
            postBody = s[0:-1]
            params = postBody.encode(encoding='UTF8')
            # time.sleep(0.1)
            # print(params)

            while True:
                try:
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request, params, timeout=30)
                    content = response.read().decode("utf-8")
                    response.close()
                    break
                except (socket.timeout, urllib.error):
                    pass
            # print(content)

            if content:
                return content
            else:
                return ''
        except ValueError:
            return None
        except (socket.timeout, urllib.error):
            pass
