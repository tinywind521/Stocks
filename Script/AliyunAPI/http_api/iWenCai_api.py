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
    # tokenMainHost = 'http://www.iwencai.com/stockpick/load-data?preParams=&ts=1&f=1&querytype=&searchfilte=&tid=stockpick&qs=zxmcxh&typed=0&selfsectsn=&queryarea='
    tokenMainHost = 'http://www.iwencai.com/stockpick/load-data?'
    tokenRefererHost = 'https://www.iwencai.com/stockpick/search?'
    # tokenRefererHost = 'https://www.iwencai.com/stockpick/search?preParams=&ts=1&f=1&querytype=&searchfilter=&tid=stockpick&qs=zhineng'
    # method = 'GET'
    tokenBodys = {
                'preParams': '',
                'ts': '1',
                'f': '1',
                'querytype': '',
                'searchfilte': '',
                'tid': 'stockpick',
                'qs': 'zxmcxh',
                'w': keyWord,
                'typed': '0',
                'selfsectsn': '',
                'queryarea': '',
            }
    tokenRef = {
                'query': keyWord,
                'qs': 'zhineng',
                'querytype': 'stock',
                'preParams': '',
                'ts': '1',
                'f': '1',
                'tid': 'stockpick',
           }
    tokenHeaders = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
                'Connection': 'keep-alive',
                'Host': 'www.iwencai.com',
                'hexin-v': 'Aj8_HX0jWVuzD11H7pgLlZUozhjMJJEVrXyXstEM2Vo1q1HM2fQjFr1IJwDh',
                # 'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': '',
               }
    tokenURL = tokenMainHost + urllib.parse.urlencode(tokenBodys)
    tokenReferer = tokenRefererHost + urllib.parse.urlencode(tokenRef)
    print(tokenURL)
    content = req(tokenURL, tokenBodys, tokenHeaders, tokenReferer)
    # print(content)
    # tokenAll = dict(eval(('{' + content.partition('var allResult = {')[2].partition(';\n')[0])
    #                      .replace(':true', ':True').replace(':false', ':False').replace(':null', ':None')))
    tokenAll = dict(eval((content.replace(':true', ':True').replace(':false', ':False').replace(':null', ':None'))))
    # print(tokenAll['data']['result'].keys())
    code_count = tokenAll['data']['result']['code_count']
    token = tokenAll['data']['result']['token']

    "getAllResult"
    MainHost = 'http://www.iwencai.com/stockpick/cache?'
    Referer = tokenURL
    Headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
                'Connection': 'keep-alive',
                'Host': 'www.iwencai.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
                'Upgrade-Insecure-Requests': '1',
                'Cookie': 'sp_search_last_right_status=show; other_uid=Ths_iwencai_Xuangu_pz2yqsq9umwzj46zj3sau4oed56rdvp0; other_uname=nnmo424153; user=MDp0aW55d2luZDUyMTo6Tm9uZTo1MDA6Mjg3NDE2NjUzOjUsMSw0MDs2LDEsNDA7NywxMTExMTExMTExMTAsNDA7OCwxMTExMDExMTAwMDAxMTExMTAwMTAwMDAwMSwxMjk7MzMsMDAwMTAwMDAwMDAwLDEyOTszNiwxMDAxMTExMTAwMDAxMTAwMTAxMTExMTEsMTI5OzQ2LDAwMDAxMTAwMTAwMDAwMTExMTExMTExMSwxMjk7NTEsMTEwMDAwMDAwMDAwMDAwMCwxMjk7NTgsMDAwMDAwMDAwMDAwMDAwMDEsMTI5Ozc4LDEsMTI5Ozg3LDAwMDAwMDAwMDAwMDAwMDAwMDAxMDAwMCwxMjk7NDQsMTEsNDA6MjQ6OjoyNzc0MTY2NTM6MTUxMjkxMDQ5Mzo6OjE0MzYxMDAzNjA6MjI3MTA3OjA6MThhYWM1YTJjNTdiYWVjYjM2ZjgxOGEzZDBkMTQ5ODYwOmRlZmF1bHRfMjow; userid=277416653; ticket=6e35a17b4c476a8bfaae5986d2da4589; ver_mark=c; guideState=1; v=Avz81JqSiqKV0b5-wSd4XMqpzZGr9aAfIpm049Z9COfKoZKF_gVwr3KphHIm; PHPSESSID=6464cb3615f41f7b7eae2c72e82f5052; cid=k44e4lnbm2er4l12pakhivkmd11503929938; ComputerID=k44e4lnbm2er4l12pakhivkmd11503929938'
                # 'X-Requested-With': 'XMLHttpRequest',
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
        time.sleep(5)
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
            # content = requests.get(url, headers=headers, allow_redirects=False).text
            r = requests.get(url, headers=headers, allow_redirects=False)
            # if headers['Cookie']:
            #     # r = requests.get(url, headers=headers, cookies=headers['Cookie'], allow_redirects=False)
            #     r = requests.get(url, headers=headers, cookies=headers['Cookie'])
            # else:
            #     # r = requests.get(url, headers=headers, allow_redirects=False)
            #     r = requests.get(url, headers=headers)
            # print(r.status_code)
            content = r.text
            # print(content)
            if content:
                return content
            else:
                return ''
        except ValueError:
            return None
        except (socket.timeout, urllib.error):
            pass


def reqDetail(url, data, headers, referer=None):
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
            request.add_header('allow_redirects',
                               'False')
            while True:
                try:
                    response = urllib.request.urlopen(request, timeout=5)
                    response.close()
                    responseHeader = dict(response.info().items())
                    print(responseHeader)
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
            print(cookie)
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
    # Referer = arg['Referer']
    Referer = None
    objResult = arg['objResult']
    # print('URL', URL)
    # print('Referer', Referer)
    # print('Headers', Headers)
    while True:
        try:
            content = req(URL, Bodys, Headers, Referer)
            r = json.loads(content)
            # for k in r:
            #     print(k)
            break
        except json.decoder.JSONDecodeError:
            # print(content)
            time.sleep(10)
            pass
    objResult.setResultArrayExtend(r['result'])
    objResult.setTitle(r['title'])


def view_bar(num, total):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    r = '\r[%s%s] %2.2f%% %d/%d' % ("|"*flow, " "*(100-flow), rate_num, num, total)
    sys.stdout.write(r)
    sys.stdout.flush()
