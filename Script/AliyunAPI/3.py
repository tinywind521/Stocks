from stock_Class.MySQL import MySQL

import pymysql

stocks_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'star2249',
    'db': 'stocks',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}
result60 = {'101': []}
# sDB for stocksDatabase
sDB = MySQL(stocks_config)
result60['101'] = [
                    {'code': '600010'},
                    {'code': '000011'},
                    {'code': '600012'},
                    {'code': '600010'},
                    {'code': '300010'},
                    {'code': '300012'},
                    {'code': '600017'},
                    {'code': '000012'},
                    {'code': '600018'},
                    ]

for i in result60['101']:
    print(i['code'])
    if i['code'][0] == '6':
        code = i['code'] + '.SH'
    elif i['code'][0] == '0' or i['code'][0] == '3':
        code = i['code'] + '.SZ'
    else:
        code = ''
    sql = "replace dailypreselect1 SET gid='" + code + "';"
    print(sql)
    sDB.execTXSQL(sql)
    print(sDB.dbReturn)
