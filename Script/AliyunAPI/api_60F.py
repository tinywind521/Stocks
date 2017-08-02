#   import urllib.request
#   Python 3.x 已经不使用urllib2了，改为urllib.request

#   import sys
#   import ssl
#   import tkinter.filedialog
#   import json

from http_api import aliyun_api
from file_io import txt

code = input("Please enter code:")
beginDay = input("Please enter beginDay:")
timeType = '60'
qType = 'bfq'
path = 'Z:/Test/60F/' + code + '.txt'
appcode = 'c7689f18e1484e9faec07122cc0b5f9e'

text = aliyun_api.realtime(code, beginDay, timeType, qType, appcode)
txt.txt_write(text, path)

