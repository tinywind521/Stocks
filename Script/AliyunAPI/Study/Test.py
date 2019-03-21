pre_close = float(input('pre_close: '))
close = float(input('close: '))
print(round(100*(close - pre_close) / pre_close, 2))
if round(100*(close - pre_close) / pre_close, 2) > 10:
    print('Limit!!!')