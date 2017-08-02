from http_api import sina_api
from functions import getValue, function

a = getValue.get_blockList_showapi()
# print(a)

for i in a:
    print(i)
    b = getValue.get_blockStocks_showapi(i['code'])
    print(len(b['block_stocksList']))
    print(b)
    print('\n')
