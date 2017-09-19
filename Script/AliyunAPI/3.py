import pymysql
from stock_Class.MySQL import MySQL

from functions import getValue


for i in getValue.get_timeLine3Days_qtimq('600173'):
    print(i)
