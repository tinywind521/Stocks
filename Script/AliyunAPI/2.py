from functions import getValue
from functions import function
from http_api import aliyun_api
import json
import numpy




code1 = '600215'
day1 = '1'

s = function.return_timeline(code1, day1)
print(s)

