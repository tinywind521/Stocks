from functions import getValue
from functions import function
from http_api import aliyun_api
import json
import numpy




code1 = '600215'
day1 = 5

s = getValue.get_timeline(code1, day1)
for k in s:
    print(k)

