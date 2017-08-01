import urllib.request
import urllib.error
import urllib.parse
import json
import sys
import ssl


def req(url, data, referer=None, **headers):
    """

    :param url:
    :param data:
    :param referer:
    :param headers:
    :return:
    """
    try:
        request = urllib.request.Request(url)
        request.add_header('Content-Type',
                           'application/x-www-form-urlencoded; charset=UTF-8')
        # request.add_header('X-Requested-With',
        #                    'XMLHttpRequest')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/58.0.3029.110 Safari/537.36')
        request.add_header('Accept',
                           'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Encoding',
                           'gzip, deflate')
        request.add_header('Accept-Language',
                           'zh-CN,zh;q=0.8')
        request.add_header('Cache-Control',
                           'max-age=0')
        request.add_header('Connection',
                           'keep-alive')
        request.add_header('Content-Length',
                           '1680')
        request.add_header('Cookie',
                           'TS0161f2e5=01412592769635b8e277eac3ffd2fe41e9c288d5aaf9107babd96d4862134857f6ccb7d32d')
        request.add_header('Host',
                           'www.hkexnews.hk')
        request.add_header('Origin',
                           'http://www.hkexnews.hk')
        # request.add_header('Referer',
        #                    'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?')
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
        # try:
        # postBody =
        params = postBody.encode(encoding='UTF8')
        response = urllib.request.urlopen(request, params)
        # except urllib.error.HTTPError or urllib.error.URLError or TimeoutError:
        #     response = None
        # print(response)
        content = response.read().decode("utf-8")
        response.close()
        if content:
            return content
        else:
            return ''
    except ValueError:
        return None
