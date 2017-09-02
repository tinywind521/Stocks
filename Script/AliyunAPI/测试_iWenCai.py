from http_api import iWenCai_api
from file_io import dict2CSV
import time

path = 'Z:\Test\Test.csv'
date = time.strftime("%Y%m%d", time.localtime())
keyWord = date + ',股票简称,涨跌幅,开盘价不复权,最高价不复权,最低价不复权,收盘价不复权,开盘价前复权,' \
                 '最高价前复权,最低价前复权,收盘价前复权,成交量(股),换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值'
r = iWenCai_api.get_iWenCai(keyWord)
print()
if len(r['results']) == r['length']:
    print('All the data(s) has been fetched!')
    dict2CSV.writeWenCaiHeader(path, r['title'])
    dict2CSV.writeWenCaiRow(path, r['results'])
else:
    print('Data(s) is incorrect!')
