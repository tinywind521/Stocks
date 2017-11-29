import urllib.request
import urllib.error
import urllib.parse
import socket
import math
import json
import time
import sys
import requests

from stock_Class.ResultDeal import ResultDeal
from multiprocessing.dummy import Pool as ThreadPool


def get_iWenCai(keyWord, PoolLength=1):
    """
    1、获取iWenCai 抓包的Token代码数据；
    2、分页抓取相关数据，多线程。
    :return:
    """

    "getToken"
    tokenMainHost = 'https://www.iwencai.com/stockpick/robot-search?'
    # tokenMainHost = 'http://www.iwencai.com/stockpick/search?'
    tokenRefererHost = 'http://www.iwencai.com/data-robot/extraction?'
    # method = 'GET'
    tokenBodys = {
                'preParams': '',
                'ts': '1',
                'f': '1',
                'verticalType': 'iwencai',
                'querytype': 'stock',
                'searchfilte': '',
                'tid': 'stockpick',
                'qs': 'zhineng',
                'w': keyWord,
                'isDataRobot': '',
            }
    tokenRef = {
                'query': keyWord,
                'querytype': 'stock',
           }
    tokenHeaders = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Host': 'www.iwencai.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.1.3071.115 Safari/537.36',
               }
    tokenURL = tokenMainHost + urllib.parse.urlencode(tokenBodys)
    tokenReferer = tokenRefererHost + urllib.parse.urlencode(tokenRef)
    print(tokenURL)
    content = req(tokenURL, tokenBodys, tokenHeaders, tokenReferer)
    # print(content)
    tokenAll = dict(eval(('{' + content.partition('var allResult = {')[2].partition(';\n')[0])
                         .replace(':true', ':True').replace(':false', ':False').replace(':null', ':None')))
    code_count = tokenAll['code_count']
    token = tokenAll['token']

    "getAllResult"
    MainHost = 'http://www.iwencai.com/stockpick/cache?'
    Referer = tokenURL
    Headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Host': 'www.iwencai.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            }

    # PoolLength = 10
    perPage = 70
    pages = int(math.ceil(code_count / perPage))
    rd = ResultDeal()
    p = 1
    for i in range(0, pages, PoolLength):
        args = []
        for j in range(0, PoolLength):
            if p > pages:
                break
            Bodys = {
                        'token': token,
                        'p': format(p, 'd'),
                        'perpage': format(perPage, 'd'),
                    }
            # print(p)
            view_bar(p, pages)
            p += 1
            URL = MainHost + urllib.parse.urlencode(Bodys)
            arg = {
                   'objResult': rd,
                   'URL': URL,
                   'Bodys': Bodys,
                   'Headers': Headers,
                   'Referer': Referer,
                   }
            args.append(arg)
        pool = ThreadPool(PoolLength)
        pool.map(getAll, args)
        pool.close()
        pool.join()
        time.sleep(1)
    results = {'title': rd.getTitle(), 'results': rd.getArrayResultValue(), 'length': code_count}
    return results


def req(url, data, headers, referer=None):
    """

    :param url:
    :param data:
    :param referer:
    :param headers:
    :return:
    """
    while True:
        try:
            # print('hehehehe', requests.get(url, headers=headers, allow_redirects=False).text)
            request = urllib.request.Request(url)
            request.add_header('Connection',
                               'keep-alive')
            request.add_header('allow_redirects',
                               'False')
            while True:
                try:
                    response = urllib.request.urlopen(request, timeout=5)
                    response.close()
                    responseHeader = dict(response.info().items())
                    # print(responseHeader)
                    try:
                        cookie = responseHeader['Set-Cookie']
                    except (KeyError, TypeError):
                        raise KeyError('Refresh iWenCai Link!')
                    # print(cookie)
                    # response.close()
                    break
                except socket.timeout or urllib.error:
                    pass
            # time.sleep(0.1)
            # print(cookie)
            request.add_header('Cookie',
                               cookie)
            if referer:
                request.add_header('Referer', referer)
            if headers:
                for k in headers.keys():
                    request.add_header(k, headers[k])
            # s = ''
            # for element in data:
            #     s += element + '=' + data[element] + '&'
            # postBody = s[0:-1]
            # params = postBody.encode(encoding='UTF8')
            # time.sleep(0.1)
            # print(params)

            while True:
                try:
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request, timeout=30)
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


def getAll(arg):
    URL = arg['URL']
    Bodys = arg['Bodys']
    Headers = arg['Headers']
    Referer = arg['Referer']
    objResult = arg['objResult']
    content = req(URL, Bodys, Headers, Referer)
    r = json.loads(content)
    # for k in r:
    #     print(k)
    objResult.setResultArrayExtend(r['result'])
    objResult.setTitle(r['title'])


def view_bar(num, total):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    r = '\r[%s%s] %2.2f%% %d/%d' % ("|"*flow, " "*(100-flow), rate_num, num, total)
    sys.stdout.write(r)
    sys.stdout.flush()
