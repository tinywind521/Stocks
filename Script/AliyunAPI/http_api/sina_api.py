#   import urllib.request
#   import sys
#   import ssl

from http_api import sina_request
from functions import function, getValue


def timeline(codeList):
    """
    获取Sina分时数据
    :param codeList:
    :return:
    """
    host = 'http://hq.sinajs.cn/list='
    # path = '/timeline'
    method = 'GET'
    bodys = {}
    codeStr = ''
    for code in codeList:
        codeStr += code + ','
    codeStr.rstrip()
    codeStr = codeStr.rpartition(',')[0]
    url = host + codeStr

    content = sina_request.req(url)
    return content
