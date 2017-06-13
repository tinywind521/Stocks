import urllib.request, sys, ssl
#Python 3.x 已经不使用urllib2了，改为urllib.request

import tkinter.filedialog
import json

from aliyun import aliyun_api
from file_io import txt

code = input("Please enter code:")
day = input("Please enter day:")
beginDay = input("Please enter beginDay:")
#   timeType = input("Please enter beginDay:")
timeType = '60'
qType = 'bfq'

#   path = input("Please enter path:")
#   path = tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])

appcode = 'c7689f18e1484e9faec07122cc0b5f9e'

#   text = aliyun_api.timeline(code, day, appcode)
text = aliyun_api.realtime(code, beginDay, timeType, qType, appcode)
print(text)
