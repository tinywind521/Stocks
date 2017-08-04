import urllib.request
import urllib.error
import urllib.parse
import socket
import time
import requests



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
                    response = urllib.request.urlopen(request, timeout=2)
                    response.close()
                    responseHeader = dict(response.info().items())
                    cookie = responseHeader['Set-Cookie']
                    ContentLength = int(responseHeader['Content-Length'])
                    # response.close()
                    break
                except socket.timeout or urllib.error:
                    pass
            # time.sleep(0.1)
            # print(cookie)

            request.add_header('Host',
                               'www.hkexnews.hk')
            request.add_header('Content-Type',
                               'application/x-www-form-urlencoded')
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/59.0.3071.115 Safari/537.36')
            request.add_header('Accept',
                               'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
            request.add_header('Accept-Encoding',
                               'gzip, deflate')
            request.add_header('Accept-Language',
                               'zh-CN,zh;q=0.8')
            request.add_header('Cache-Control',
                               'max-age=0')
            request.add_header('Connection',
                               'keep-alive')
            request.add_header('Content-Length',
                               format(int(ContentLength / 440), 'd'))
            request.add_header('Cookie',
                               (cookie.split(';'))[0])
            request.add_header('Host',
                               'www.hkexnews.hk')
            request.add_header('Origin',
                               'http://www.hkexnews.hk')
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
                    response = urllib.request.urlopen(request, params, timeout=5)
                    content = response.read().decode("utf-8")
                    response.close()
                    break
                except socket.timeout or urllib.error:
                    pass
            # content = requests.get(url).text
            # print(content)

            if content:
                return content
            else:
                return ''
        except ValueError:
            return None
        except socket.timeout or urllib.error:
            pass
