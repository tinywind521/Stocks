from functions import getValue
from functions import function
from http_api import aliyun_api
import json
import numpy


def return_timeline(code, day, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    try:
        text = aliyun_api.timeline(code, day, appcode)
        all_dict = json.loads(text)
        print(all_dict)
        showapi_res_body = all_dict['showapi_res_body']
        dataList = showapi_res_body['dataList']
        # print(dataList)
        for dataElement in dataList:
            # print(dataElement)
            date = dataElement['date']
            lastclose = dataElement['yestclose']
            length = dataElement['count']
            timeline = dataElement['minuteList']
            # print(len(timeline))
            print(date)
            if len(timeline) == int(length):
                for ss in timeline:
                    print(ss)
    except ValueError:
        return None

code1 = '600215'
day1 = '1'

s = return_timeline(code1, day1)
print(s)

