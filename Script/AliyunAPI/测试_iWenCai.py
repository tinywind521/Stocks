from http_api import iWenCai_api
from file_io import dict2CSV
import time

rootPath = 'Z:/Output/'
# rootPath = 'Z:/Test/'
addName = '.csv'

# 自动和手动日期切换
date = time.strftime("%Y%m%d", time.localtime())
# date = '20171020'
print(date)
lastDate = input("Input last date (20170101): ")

keyWords = [
                {
                    'keyWord': date + ',股票简称,涨跌幅,开盘价不复权,最高价不复权,'
                                      '最低价不复权,收盘价不复权,开盘价前复权,'
                                      '最高价前复权,最低价前复权,收盘价前复权,成交量,'
                                      '换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值',
                    # 'keyWord': date + ',股票简称,涨跌幅,开盘价不复权,最高价不复权,'
                    #                   '最低价不复权,收盘价不复权,'
                    #                   '成交量,'
                    #                   '换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值',
                    'fileName': date + '_data' + addName,
                    'name': 'data',
                    'PoolLength': 10
                },
                {
                    'keyWord': lastDate + '的大宗交易笔数',
                    'fileName': lastDate + '_lastDateDZ' + addName,
                    'name': 'dz',
                    'PoolLength': 1
                },
                {
                    'keyWord': date + '的大宗交易笔数',
                    'fileName': date + '_dz' + addName,
                    'name': 'dz',
                    'PoolLength': 1
                },
                {
                    'keyWord': date + '的龙虎榜',
                    'fileName': date + '_lhb' + addName,
                    'name': 'lhb',
                    'PoolLength': 1
                },
                {
                    'keyWord': date + '的所属行业,' + date + '的所属概念,',
                    'fileName': date + '_pc' + addName,
                    'name': 'pc',
                    'PoolLength': 10
                },
                {
                    'keyWord': date + '的涨停,' + date + '的首次涨停时间,' + date + '的最终涨停时间',
                    'fileName': date + '_limitup' + addName,
                    'name': 'limitup',
                    'PoolLength': 1
                },
                {
                    'keyWord': date + '的曾涨停',
                    'fileName': date + '_unlimitup' + addName,
                    'name': 'unlimitup',
                    'PoolLength': 1
                },
                {
                    'keyWord': date + '的营业部名称',
                    'fileName': date + '_YYB' + addName,
                    'name': 'YYB',
                    'PoolLength': 1
                },
                {
                    'keyWord': date + '的交易状态是可交易，' + date + '的不是新股，' + date + '的交易状态不包含停牌',
                    'fileName': 'daily' + addName,
                    'name': 'daily',
                    'PoolLength': 10
                },
            ]
# keyWords = date + ',股票简称,涨跌幅,开盘价不复权,最高价不复权,最低价不复权,收盘价不复权,开盘价前复权,' \
#                  '最高价前复权,最低价前复权,收盘价前复权,成交量(股),换手率(%),振幅,上市不超过，上市天数,技术形态,A股流通市值'
for keyWord in keyWords:
    print('Fetching ' + date + ' ' + keyWord['name'] + '...')
    r = iWenCai_api.get_iWenCai(keyWord['keyWord'], keyWord['PoolLength'])
    print()
    # print(len(r['results']))
    # print(r['length'])
    if len(r['results']) >= r['length'] and r['length']:
        print('All the ' + keyWord['name'] + ' data(s) has been fetched!')
        path = rootPath + keyWord['fileName']
        dict2CSV.writeWenCaiHeader(path, r['title'])
        dict2CSV.writeWenCaiRow(path, r['results'])
    else:
        # print(r)
        print('Data(s) is incorrect!')
