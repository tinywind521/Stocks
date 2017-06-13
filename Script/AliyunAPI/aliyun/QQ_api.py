import json
from aliyun import QQ_request


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
    content = json.loads(QQ_request.req(url).partition('=')[2].replace('_', '"').replace(':', '":').replace(';', ''))
    result = []
    for array in content['datas']:
        tempdict = {'date': '', 'code': '', 'name': '', 'type': '', 'typeid': '', 'close': '', 'zf': ''}
        i = 0
        for k in tempdict.keys():

            if k.find('date') != -1:
                tempdict[k] = array[i].replace('-', '')
            else:
                tempdict[k] = array[i]
            i+=1
        result.append(tempdict)

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
    content = json.loads(QQ_request.req(url).partition('=')[2].replace('_', '"').replace(':', '":').replace(';', ''))
    result = []
    for array in content['datas']:
        tempdict = {'code': '', 'name': '', 'bs': '', 'no': '', 'date': '', 'yyname': '', 'yybuy': '', 'yysell':''}
        i = 0
        for k in tempdict.keys():

            if k.find('date') != -1:
                tempdict[k] = array[i].replace('-', '')
            else:
                tempdict[k] = array[i]
            i+=1
        result.append(tempdict)

    return result