import time
import os
import json

from file_io import txt, jsonFiles
from functions import getValue
from stock_Class.stock import Stock, Yline

allBlockCode = getValue.get_blockList_showapi()
allBlockList = []
for BlockList in allBlockCode:
    BlockListReturn = getValue.get_blockStocks_showapi(BlockList['code'])
    if BlockListReturn:
        allBlockList.append(BlockListReturn)

# 写入 JSON 数据
outputRootPath = 'Z:/Test'
path = outputRootPath + '/allBlockList.json'
jsonFiles.Write(path, allBlockList)

allBlockList = jsonFiles.Read(path)
