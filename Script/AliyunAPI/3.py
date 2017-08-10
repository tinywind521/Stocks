from http_api import sina_api
from functions import getValue, function

a = getValue.get_blockList_showapi()
# print(a)

for i in a:
    # print(i)
    b = getValue.get_blockStocks_showapi(i['code'])
    # print(len(b['block_stocksList']))
    print(b)
    # print('\n')

# allBlockCode = getValue.get_blockList_showapi()
# allBlockList = []
# for BlockList in allBlockCode:
#     b = getValue.get_blockStocks_showapi(BlockList['code'])
#     allBlockList.append(b)
#     print(b)
# print(allBlockList)
