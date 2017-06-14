from functions import getValue
from aliyun import aliyun_api
import json


def get_realtimeValue(aliyun_input):
    realtimeValue = aliyun_input['showapi_res_body']['dataList']
    return realtimeValue

b = getValue.get_dateList('20170101', 10)
print(b)
aliyun_str = aliyun_api.realtime('000001', b[0], '60')
aliyun_dict = json.loads(aliyun_str)
print(aliyun_str)

s = get_realtimeValue(aliyun_dict)
s.reverse()
print(len(s))
for element in s:
    print(element)

# 根据日期列表，按照日期，重新计算60F，因为集合竞价问题
# 前阴连阴，连阴后必须连阳，再阴；双阴必须前低后高
# 中间的连阳可以假阳
# 前后都是连阴形态，也要考虑
# 中轨怎么考虑



# print(c)

# def ss(string=[]):
#     for s in string:
#         print(s)
#     return None
# try:
#     d = input('Input Reference: ')
#     dd = list(d)
#     print(dd)
#     ss(dd)
# except:
#     print('Ref Error!')