# python3.5
import urllib.request
import urllib.error
import socket
import time


def req(url, sleepTime=0.1):
    """
    aliyun API
    :param sleepTime:
    :param url:
    :return:
    """

    url.encode('utf-8')
    # print(url)
    socket.setdefaulttimeout(20)
    content = None
    for i in range(5):
        try:
            try:
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request, timeout=15)
                # print(response)
                # response = urllib.request.urlopen(request)
                # time.sleep(0.1)
                content = response.read().decode("utf-8")
                response.close()
                break
            except (BaseException, socket.error, OSError):
                print(url)
                return ''
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionAbortedError,
                OSError, AttributeError, KeyError, ValueError):
            time.sleep(5)
            print('Oh,Let me have a rest! 5S!')
    if content:
        time.sleep(sleepTime)
        return content
    else:
        return ''
