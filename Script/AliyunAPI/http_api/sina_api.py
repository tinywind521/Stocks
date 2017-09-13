#   import urllib.request
#   import sys
#   import ssl

from http_api import sina_request
from functions import function, getValue

# http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var%20_sh603901_5_1505264471270=/CN_MarketData.getKLineData?symbol=sh603901&scale=5&ma=no&datalen=1023


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
