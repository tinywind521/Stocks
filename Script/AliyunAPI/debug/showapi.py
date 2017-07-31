# python3.5
import urllib.request
import urllib.error
import urllib.parse
import sys
import ssl
import time
import json

"""
6a09e5fe3e724252b35d571a0b715baa
"""

print('send data....')
showapi_appid = "31351"
showapi_sign = "6a09e5fe3e724252b35d571a0b715baa"
url = "http://route.showapi.com/131-50"
send_data = urllib.parse.urlencode(
    [
        ('showapi_appid', showapi_appid),
        ('showapi_sign', showapi_sign),
        ('code', "600004"),
        ('time', "60"),
        ('beginDay', "20170701"),
        ('type', "bfq")
    ])
print(send_data)
req = urllib.request.Request(url)
print(url)
f = urllib.request.urlopen(req, data=send_data.encode('utf-8'))
print('Status:', f.status, f.reason)
str_res = f.read().decode('utf-8')
print('str_res:', str_res)
json_res = json.loads(str_res)
print('json_res data is:', json_res)