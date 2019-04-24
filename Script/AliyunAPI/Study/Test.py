import time

a = time.strptime('2017/7/6', '%Y/%m/%d')
b = time.strftime('%Y%m%d', a)
print(b)