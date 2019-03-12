import tushare as ts
token = 'c48302b906aab9cf3ce6a8279edb75756646204934f69863754ba7a7'
ts.set_token(token)

"""
https://www.cnblogs.com/hdulzt/p/7067187.html
https://tushare.pro/
ts_code	str	
trade_date	str	
open	float	
high	float	
low	float	
close	float	
pre_close	float	
change	float	
pct_chg	float	 
vol	float	 
amount	float	 
"""

pro = ts.pro_api()
data = pro.query('stock_basic', exchange='', list_status='L', fields='symbol')
# df = pro.daily(trade_date='20180810')
df = pro.daily(ts_code='000001.SZ',fields='ts_code, open, pre_close')
print(df)

# for i in data['symbol']:
#     print(i)
# print(df)
