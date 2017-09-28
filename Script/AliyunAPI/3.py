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
sql = 'truncate table dailypreselect;'
sDB.execTXSQL(sql)
sDB.commit()
