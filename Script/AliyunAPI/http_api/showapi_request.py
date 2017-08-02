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


def req(url, sleepTime=0.2):
    """
    aliyun API
    :param sleepTime:
    :param url:
    :return:
    """

    url.encode('utf-8')
    # print(url)
    socket.setdefaulttimeout(20)
    # or socket.timeout
    content = None
    for i in range(5):
        try:
            h = None
            try:
                request = urllib.request.Request(url)
                h = request.headers
                response = urllib.request.urlopen(request, timeout=20)
                # print(response)
                # response = urllib.request.urlopen(request)
                # time.sleep(0.1)
                content = response.read().decode("utf-8")
                response.close()
                break
            except BaseException or socket.error or OSError:
                print(h)
                return ''
        except urllib.error.HTTPError or urllib.error.URLError or TimeoutError or ConnectionAbortedError \
                or OSError or AttributeError or KeyError or ValueError:
            time.sleep(5)
            print('Oh,Let me have a rest! 5S!')
    if content:
        time.sleep(sleepTime)
        return content
    else:
        return ''
