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
    socket.setdefaulttimeout(10)
    content = None
    for i in range(10):
        try:
            try:
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request, timeout=10)
                content = response.read().decode("utf-8")
                response.close()
                break
            except (BaseException, socket.error, OSError):
                print('\n')
                print(url)
                # return ''
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionAbortedError,
                OSError, AttributeError, KeyError, ValueError):
            time.sleep(2)
            # print('Oh,Let me have a rest! 2S!')
    if content:
        time.sleep(sleepTime)
        return content
    else:
        return ''
