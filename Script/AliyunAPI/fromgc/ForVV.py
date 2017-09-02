import urllib.request
import urllib.error
import urllib.parse
import socket
import math
import json
import time
import sys

"""多线程库"""
from multiprocessing.dummy import Pool as ThreadPool


# """多线程使用到的对象"""
class ResultDeal:
    def __init__(self):
        self._result = []
        self._title = None

    def setResultAppend(self, tempArg):
        self._result.extend(tempArg)

    def getResultValue(self):
        return self._result

    def setTitle(self, title):
        if self._title:
            pass
        else:
            self._title = title

    def getTitle(self):
        return self._title


# """主要爬虫功能函数"""
def get_iWenCai(keyWordIn):
    """
    1、获取iWenCai 抓包的Token代码数据；
    2、分页抓取相关数据，多线程。
    :return:
    """

    "getToken"
    tokenMainHost = 'http://www.iwencai.com/rapid/entry-search?'
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
        'w': keyWordIn,
        'isDataRobot': '',
    }
    tokenRef = {
        'query': keyWordIn,
        'querytype': 'stock',
    }
    tokenHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.iwencai.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    tokenURL = tokenMainHost + urllib.parse.urlencode(tokenBodys)
    tokenReferer = tokenRefererHost + urllib.parse.urlencode(tokenRef)
    print(tokenURL)
    content = req(tokenURL, tokenBodys, tokenHeaders, tokenReferer)
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

    PoolLength = 10
    perPage = 70
    pages = int(math.ceil(code_count / perPage))
    r = ResultDeal()
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
                'objResult': r,
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
    results = {'title': r.getTitle(), 'results': r.getResultValue(), 'length': code_count}
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
            request = urllib.request.Request(url)
            request.add_header('Connection',
                               'keep-alive')
            while True:
                try:
                    response = urllib.request.urlopen(request, timeout=5)
                    response.close()
                    responseHeader = dict(response.info().items())
                    # print(responseHeader)
                    try:
                        cookie = responseHeader['Set-Cookie']
                    except (KeyError, TypeError):
                        raise KeyError('如果你看到了我，请点击上方链接输一下验证码!')
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
    Bodys = arg['URL']
    Headers = arg['Bodys']
    Referer = arg['Referer']
    objResult = arg['objResult']
    content = req(URL, Bodys, Headers, Referer)
    r = json.loads(content)
    # for k in r:
    #     print(k)
    objResult.setResultAppend(r['result'])
    objResult.setTitle(r['title'])


# """进度条函数"""
def view_bar(num, total):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    s = '\r[%s%s] %2.2f%% %d/%d' % ("|"*flow, " "*(100-flow), rate_num, num, total)
    sys.stdout.write(s)
    sys.stdout.flush()


# """CSV写入函数"""
def writeWenCaiHeader(filePath, headers, method='w+'):
    try:
        f = open(filePath, method)
        text = ''
        end = headers.pop()
        for s in headers:
            text = text + s + ','
        text = (text + end + '\n').replace('\r', '')
        f.write(text)
        f.close()
    except ValueError:
        pass


def writeWenCaiRow(filePath, rows):
    try:
        f = open(filePath, 'a+')
        for row in rows:
            text = ''
            end = row.pop()
            for s in row:
                text = text + str(s).replace(',', '') + ','
            text = text + end + '\n'
            f.write(text)
        f.close()
    except ValueError:
        pass


# 保存路径
path = 'Z:\Test\Test.csv'

# 搜索关键字
date = time.strftime("%Y%m%d", time.localtime())
keyWord = date + ',股票简称,涨跌幅,开盘价不复权,最高价不复权,最低价不复权,收盘价不复权,开盘价前复权,' \
                 '最高价前复权,最低价前复权,收盘价前复权,成交量(股),换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值'

# 如果需要使用其他日期请用这里
# keyWord = '-> 这里是日期哟 <-,股票简称,涨跌幅,开盘价不复权,最高价不复权,最低价不复权,收盘价不复权,开盘价前复权,最高价前复权,最低价前复权,' \
# '收盘价前复权,成交量(股),换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值'

results = get_iWenCai(keyWord)
print()
if len(results['results']) == results['length']:
    print('抓包成功！')
    writeWenCaiHeader(path, results['title'])
    writeWenCaiRow(path, results['results'])
else:
    print('抓包失败！')
