from string import capwords
a = {'min': 10.7, 'open': 10.72, 'volumn': 62789.0, 'time': '20170630'}
suba = ['min', 'open']
b = dict([(key, a[key]) for key in suba])
print(b)

print(list(a.values()))
print(list(a.keys()))
s = ''

a = capwords('a bd def ghijk', ' ')