import json
from http_api import QQ_request
import operator
import urllib.error


def lhb_code_list(code):
    """
    个股历史龙虎榜
    :return:
    """
    host = 'http://stock.finance.qq.com/cgi-bin'
    path = '/sstock/q_lhb_js'
    method = 'GET'
    querys = 't=' + '1' + '&c=' + code
    bodys = {}
    url = host + path + '?' + querys
    result = []
    QQ_return = None
    content = {}
    try:
        try:
            try:
                QQ_return = QQ_request.req(url).replace('\n', '')
            except TimeoutError or urllib.error.URLError:
                QQ_return = QQ_request.req(url).replace('\n', '')
            content = json.loads(QQ_return.partition('=')[2].replace('_', '"').replace(':', '":').replace(';', ''))
        except ValueError or AttributeError or json.decoder.JSONDecodeError or TimeoutError or urllib.error.URLError:
            print('lhb_code_list Error!')
            print(url)
            print(QQ_return)
            print(content)
            return result
        # keyList = {'curpage', 'pages', 'num'}
        # p = {key: value for key, value in content.items() if key in keyList}
        # print(p)
        pages = content['pages']
        for page in range(0, pages):
            if page != 0:
                querys = 't=' + format((page + 1), 'd') + '&c=' + code
                url = host + path + '?' + querys
                try:
                    QQ_return = QQ_request.req(url).replace('\n', '')
                except TimeoutError or urllib.error.URLError:
                    QQ_return = QQ_request.req(url).replace('\n', '')
                content = json.loads(QQ_return.partition('=')[2].replace('_', '"').replace(':', '":').replace(';', ''))
            j = 0
            max_j = content['num']
            for array in content['datas']:
                tempdict = {'date': '', 'code': '', 'name': '', 'type': '', 'typeid': '', 'close': '', 'zf': ''}
                i = 0
                if j == max_j:
                    break
                else:
                    j += 1
                for k in tempdict.keys():
                    if k.find('date') != -1:
                        tempdict[k] = array[i].replace('-', '')
                    else:
                        tempdict[k] = array[i]
                    i += 1
                result.append(tempdict)
    except json.decoder.JSONDecodeError or ValueError or AttributeError or TimeoutError or urllib.error.URLError:
        print('lhb_code_list Error!')
        print(url)
        print(QQ_return)
        print(content)
        return result
    return result


def lhb_code_detail(code, date, title, typeid):
    """
    个股龙虎榜当日明细
    :return:
    """
    host = 'http://stock.finance.qq.com/cgi-bin'
    path = '/sstock/q_lhb_xx_js'
    method = 'GET'
    querys = 't=' + title + '&c=' + code + '&b=' + date + '&l=' + typeid
    bodys = {}
    url = host + path + '?' + querys
    result = []
    QQ_return = None
    content = {}
    try:
        try:
            QQ_return = QQ_request.req(url).replace('\n', '')
        except TimeoutError or urllib.error.URLError:
            QQ_return = QQ_request.req(url).replace('\n', '')
        # QQ_return = QQ_request.req(url)
        content = json.loads(QQ_return.partition('=')[2].replace('_', '"').replace(':', '":').replace(';', ''))
        # print(content)
        for array in content['datas']:
            tempdict = {'code': '', 'name': '', 'bs': '', 'no': '', 'date': '', 'yyname': '', 'yybuy': '', 'yysell': ''}
            i = 0
            for k in tempdict.keys():
                if k.find('date') != -1:
                    tempdict[k] = array[i].replace('-', '')
                else:
                    tempdict[k] = array[i]
                i += 1
            result.append(tempdict)
    except json.decoder.JSONDecodeError or ValueError or AttributeError or TimeoutError or urllib.error.URLError:
        print('lhb_code_detail Error!')
        print(url)
        print(QQ_return)
        print(content)
        return []
    else:
        return result
