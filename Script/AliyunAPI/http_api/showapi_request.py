# python3.5
import urllib.request
import urllib.error
import socket
# import urllib.parse
import time

"""
6a09e5fe3e724252b35d571a0b715baa
"""

# print('send data....')
# showapi_appid = "31351"
# showapi_sign = "6a09e5fe3e724252b35d571a0b715baa"
# url = "http://route.showapi.com/131-50"
# send_data = urllib.parse.urlencode(
#     [
#         ('showapi_appid', showapi_appid),
#         ('showapi_sign', showapi_sign),
#         ('code', ""),
#         ('time', ""),
#         ('beginDay', ""),
#         ('type', "")
#     ])
#
# req = urllib.request.Request(url)
# f = urllib.request.urlopen(req, data=send_data.encode('utf-8'))
# print('Status:', f.status, f.reason)
# str_res = f.read().decode('utf-8')
# print('str_res:', str_res)
# json_res = json.loads(str_res)
# print('json_res data is:', json_res)


def req(url):
    """
    aliyun API
    :param url:
    :return:
    """
    try:
        url.encode('utf-8')
        # print(url)
        socket.setdefaulttimeout(30)
        content = None
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            content = response.read().decode("utf-8")
        except urllib.error.HTTPError or urllib.error.URLError or TimeoutError or ConnectionAbortedError \
                or socket.timeout or AttributeError:
            time.sleep(15)
            print('Oh,Let me have a rest! 5S!')
            try:
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)
                content = response.read().decode("utf-8")
            except urllib.error.HTTPError or urllib.error.URLError or TimeoutError or ConnectionAbortedError \
                    or socket.timeout or AttributeError:
                response = None
        # print(response)
        # try:
        #     content = response.read().decode("utf-8")
        #     # print(content)
        # except AttributeError or socket.timeout:
        #     content = ''
        if content:
            time.sleep(1)
            return content
        else:
            return ''
    except ValueError:
        return None
