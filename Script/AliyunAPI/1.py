from http_api import qtimq_api
from http_api import qtimq_request
from functions import getValue

import json
import os


tempPath = 'z:/test/codeList.txt'
codeList = []
if os.path.exists(tempPath):
    f = open(tempPath, 'r')
    text = f.read()
    f.close()
    codeList = text.splitlines()

i = 0
for code in codeList:
    i += 1

    showapi_dict = getValue.get_dayK_qtimq(code, 160, 61)
    print(showapi_dict)
    print(code, end='\t')
    print(i)
    # print(showapi_dict['data'][code]['m60'])
