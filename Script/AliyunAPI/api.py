from functions import function
from aliyun import aliyun_api

appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
s = function.return_stocklist(appcode)

f = open('z:/Test/test.csv', 'w+')
for element in s:
    tempstr = element['market'] + element['code'] + ',' + element['name'] + '\n'
    f.write(tempstr)
f.close()

# f = open('z:/Test/test.txt', 'w+')
# f.write(s[1])
# f.close()
