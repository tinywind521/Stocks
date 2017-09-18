from http_api import hkex_api
from file_io import dict2CSV
from functions import getValue
import re
import socket
import pymysql

from stock_Class.MySQL import MySQL

beginDate = input("Please input begin date (like, 20170317): ")

if not beginDate:
    stocks_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'star2249',
        'db': 'stocks',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    sDB = MySQL(stocks_config)
    sql = 'select gdate from hkex where to_days(gdate) >=' \
          ' (select to_days(gdate) from hkex group by gdate ' \
          'desc limit 4,1) group by gdate;'
    sDB.execSQL(sql)
    beginDate = sDB.dbReturn[-1]['gdate'].isoformat()
    beginDate = beginDate[0:4] + beginDate[5:7] + beginDate[8:]

dateList = getValue.get_dateList('20170317', 0)

socket.setdefaulttimeout(None)

if len(beginDate) >= 6:
    dateList = dateList[dateList.index(beginDate):]
    print(dateList)
for date in dateList:
    print(date + ' sz begin fetching...')
    s = hkex_api.hkex(date, 'sz')
    print(date + ' sz begin writing...')
    exp1 = re.compile('(?isu)<tr class="row[^>]*>(.*?)</tr>')
    exp2 = re.compile("(?isu)<td[^>]*>(.*?)</td>")
    exp3 = re.compile("(?isu)\\s+?")
    key = ['代码', '名称', '持股量', '百分比']
    result = []
    for row in exp1.findall(s):
        value = []
        # d = {}
        for col in exp2.findall(row):
            # value.append(col.replace('\r\n                                ', '')
            #              .replace('\r\n                            ', ''))
            value.append(exp3.sub('', col))
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
    exp3 = re.compile("(?isu)\\s+?")
    key = ['代码', '名称', '持股量', '百分比']
    result = []
    for row in exp1.findall(s):
        value = []
        # d = {}
        for col in exp2.findall(row):
            # value.append(col.replace('\r\n                                ', '')
            #              .replace('\r\n                            ', ''))
            value.append(exp3.sub('', col))
        d = dict(zip(key, value))
        result.append(d)
    path = 'z:/test/' + date + 'sh' + '_hkex.csv'
    dict2CSV.writeHeader(path, key)
    dict2CSV.writeRows(path, result)
    print(date + ' sh OK!')

