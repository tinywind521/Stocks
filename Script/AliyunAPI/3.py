import pymysql
from stock_Class.MySQL import MySQL

stocks_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'star2249',
    'db': 'stocks',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

# sDB for stocksDatabase
sDB = MySQL(stocks_config)
sql = 'select gid from dailypreselect;'
sDB.execSQL(sql)
dailyList = [gid['gid'][0:6] for gid in sDB.dbReturn]

