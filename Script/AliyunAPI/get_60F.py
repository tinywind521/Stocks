#   import urllib.request
#   Python 3.x 已经不使用urllib2了，改为urllib.request
#   import sys
#   import ssl
#   import tkinter.filedialog
#   import json

from aliyun import aliyun_api
from file_io import txt


def savefile(code):
    beginDay = '20170101'
#   code = input("Please enter code:")
#   beginDay = input("Please enter beginDay:")
#   timeType = input("Please enter beginDay:")
    timetype = '60'
    qtype = 'bfq'

#   path = input("Please enter path:")
#   path = tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])
    path = 'Z:/Test/60F/' + code + '.txt'
    appcode = 'c7689f18e1484e9faec07122cc0b5f9e'

    text = aliyun_api.realtime(code, beginDay, timetype, qtype, appcode)
    txt.txt_write(text, path)

path = 'Z:/Code/code.txt'
s = txt.txt_read(path)
codelist = s.splitlines()

for code in codelist:
    if len(code) == 6:
        savefile(code)
    else:
        pass
    pass
