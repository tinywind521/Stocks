from http_api import hkex_api
from file_io import dict2CSV
from functions import getValue
import re
import socket

socket.setdefaulttimeout(None)

dateList = getValue.get_dateList('20170317', 0)
beginDate = input("Please input begin date (like, 20170317): ")

if len(beginDate) >= 6:
    dateList = dateList[dateList.index(beginDate):]
    print(dateList)
for date in dateList:
    print(date + ' sz begin fetching...')
    s = hkex_api.hkex(date, 'sz')
    print(date + ' sz begin writing...')
    exp1 = re.compile('(?isu)<tr class="row[^>]*>(.*?)</tr>')
    exp2 = re.compile("(?isu)<td[^>]*>(.*?)</td>")
    key = ['代码', '名称', '持股量', '百分比']
    result = []
    for row in exp1.findall(s):
        value = []
        # d = {}
        for col in exp2.findall(row):
            value.append(col.replace('\r\n                                ', '')
                         .replace('\r\n                            ', ''))
        d = dict(zip(key, value))
        result.append(d)
    path = 'z:/test/' + date + 'sz' + '_hkex.csv'
    dict2CSV.writeHeader(path, key)
    dict2CSV.writeRows(path, result)
    print(date + ' sz OK!')

for date in dateList:
    print(date + ' sh begin fetching...')
    s = hkex_api.hkex(date, 'sh')
    print(date + ' sh begin writing...')
    exp1 = re.compile('(?isu)<tr class="row[^>]*>(.*?)</tr>')
    exp2 = re.compile("(?isu)<td[^>]*>(.*?)</td>")
    key = ['代码', '名称', '持股量', '百分比']
    result = []
    for row in exp1.findall(s):
        value = []
        # d = {}
        for col in exp2.findall(row):
            value.append(col.replace('\r\n                                ', '')
                         .replace('\r\n                            ', ''))
        d = dict(zip(key, value))
        result.append(d)
    path = 'z:/test/' + date + 'sh' + '_hkex.csv'
    dict2CSV.writeHeader(path, key)
    dict2CSV.writeRows(path, result)
    print(date + ' sh OK!')

