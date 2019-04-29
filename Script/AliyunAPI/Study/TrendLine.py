# -*- coding: utf-8 -*-
import datetime as dt
import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md


def dateFormat(date_dmy):
    return dt.datetime.strptime(str(date_dmy, encoding='utf-8'),'%d-%m-%Y').date()
#    dmy = str(dmy, encoding='utf-8')
#    date = dt.datetime.strptime(dmy, '%d-%m-%Y').date()
#    ymd = date.strftime('%Y-%m-%d')
#    return ymd

dates, opening_prices, highest_prices, lowest_prices, closing_prices = np.loadtxt(
        'stock.csv',
        delimiter=',',
        usecols=(1, 3, 4, 5, 6),
        unpack=True,
        dtype='M8[D], f8, f8, f8, f8',
        converters={1: dateFormat})

'''
# ******************************* 重要内容分割线:start *******************************
'''
# x轴横坐标 xi
# numpy.datetime64对象通过.astype(int)方法：返回自 0001-01-01 开始的第多少天
# 对比pandas相同功能的方法，详见end mark
days = dates.astype(int)

'''
A . X = B:  (m*x + n*1 = y: 
A->(x,1)组成的数组；X->(k,b)组成的数组; B-> (y)组成的数组
'''
# A == [xi,1], B == [yi], X == [parameters(k, b)]
A = np.column_stack((days, np.ones_like(days)))
# priceTrend == B -> [yi]
priceTrend = (highest_prices + lowest_prices + closing_prices) / 3
# 求解参数(k,b)组成的数组 X: X[0]=k, X[1]=b
X = np.linalg.lstsq(A, priceTrend, rcond = None)[0]         # rcond见end mark
# 趋势线线性方程 y = k*x + b  (X[0]=k, X[1]=b)
trend_line = days * X[0] + X[1]

# 波动价差
waves = highest_prices - lowest_prices

# resistance_points == B -> [yi]
resistance_points = priceTrend + waves
# 求解参数(k,b)组成的数组  X: X[0]=k, X[1]=b
X = np.linalg.lstsq(A, resistance_points, rcond = None)[0]
# 阻力线线性方程
resistance_line = days * X[0] + X[1]

# support_points == B -> [yi]
support_points = priceTrend - waves
# 求解参数(k,b)组成的数组  X: X[0]=k, X[1]=b
X = np.linalg.lstsq(A, support_points, rcond = None)[0]
# 支撑线线性方程
support_line = days * X[0] + X[1]
'''
# ******************************* 重要内容分割线:end *******************************
'''

mp.figure('lineTrend', facecolor='lightgray')
mp.title('lineTrend', fontsize=20)
mp.xlabel('date', fontsize=14)
mp.ylabel('stockPrice', fontsize=14)
ax = mp.gca()

ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MO))
ax.xaxis.set_minor_locator(md.DayLocator())
ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %Y'))

mp.tick_params(labelsize=10)
mp.grid(linestyle=':')

dates = dates.astype(md.datetime.datetime)

rise = closing_prices - opening_prices >= 0.01
fall = opening_prices - closing_prices >= 0.01
fc = np.zeros(dates.size, dtype='3f4')
ec = np.zeros(dates.size, dtype='3f4')

fc[rise], fc[fall] = (1, 1, 1), (0.85, 0.85, 0.85)
ec[rise], ec[fall] = (0.85, 0.85, 0.85), (0.85, 0.85, 0.85)

mp.bar(dates, highest_prices - lowest_prices, 0, lowest_prices, color=fc, edgecolor=ec)
mp.bar(dates, closing_prices - opening_prices, 0.8, opening_prices, color=fc, edgecolor=ec)
mp.scatter(dates, priceTrend, c = 'orange', s = 45, zorder = 2)
mp.scatter(dates, resistance_points, c = 'g', s = 45, zorder = 2)
mp.scatter(dates, support_points, c = 'r', s = 45, zorder = 2)
mp.plot(dates, trend_line, c = 'b', label='trend_line',linestyle='--')
mp.plot(dates, resistance_line, c = 'r',label='resistance_line',linestyle='--')
mp.plot(dates, support_line, c = 'g',label='support_line',linestyle='--')

mp.legend()

mp.gcf().autofmt_xdate()
mp.show()



'''
# ******************************* 重要内容分割线:start *******************************
'''
    # **************************** niubility *****************************
    # numpy.datetime64 可以直接 .astype(int) 返回据初始时间经过的天数
    # pandas中datetime模块datetime.date类和datetime.datetime类中的对象属性
    #       dt.toordinal()功能：返回日期是自 0001-01-01 开始的第多少天
'''
    a = pd.Series(['2011-01-01', '2025-02-02'])

    b = np.array(a)

    type(a),type(b)
    Out[376]: (pandas.core.series.Series, numpy.ndarray)

    type(b[1])
    Out[377]: str

    b = b.astype('M8[D]'); type(b[1])
    Out[378]: numpy.datetime64

    b
    Out[379]: array(['2011-01-01', '2025-02-02'], dtype='datetime64[D]')

    b.astype(int)
    Out[380]: array([14975, 20121])         # 返回了天数
'''
    # **************************** niubility *****************************

'''
FutureWarning: `rcond` parameter will change to the default 
of machine precision times ``max(M, N)`` where M and N 
are the input matrix dimensions.

To use the future default and silence 
this warning we advise to pass `rcond=None`, 
to keep using the old, explicitly pass `rcond=-1`.
'''
'''
# ******************************* 重要内容分割线:end *******************************
'''