d = {'min': 8.33, 'minute': '201706231030', 'open': 8.21,
     'volumn': 148719, 'time': '201706231030', 'max': 8.73,
     'close': 8.51, 'lastclose': 8.61, 'mid': 8.11,
     'upper': 8.39, 'lower': 7.83}

s = float(d['close']) - float(d['lastclose'])
print(s)
