from http_api import iWenCai_api
import json


result = iWenCai_api.hkex()
d = json.loads(result)

r = d['result']

for i in r:
    print(i)

"""
'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E8%82%A1%E7%A5%A8%E4%BB%A3%E7%A0%81%2C%E8%82%A1%E7%A5%A8%E7%AE%80%E7%A7%B0%2C%E6%B6%A8%E8%B7%8C%E5%B9%85%2C%E5%BC%80%E7%9B%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E9%AB%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E4%BD%8E%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E6%94%B6%E7%9B%98%E4%BB%B7%E4%B8%8D%E5%A4%8D%E6%9D%83%2C%E5%BC%80%E7%9B%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E9%AB%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%9C%80%E4%BD%8E%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%94%B6%E7%9B%98%E4%BB%B7%E5%89%8D%E5%A4%8D%E6%9D%83%2C%E6%88%90%E4%BA%A4%E9%87%8F(%E8%82%A1)%2C%E6%8D%A2%E6%89%8B%E7%8E%87(%25)%2C%E6%8C%AF%E5%B9%85%2C%E4%B8%8A%E5%B8%82%E4%B8%8D%E8%B6%85%E8%BF%87%EF%BC%8C%E4%B8%8A%E5%B8%82%E5%A4%A9%E6%95%B0%2C%E6%8A%80%E6%9C%AF%E5%BD%A2%E6%80%81%2CA%E8%82%A1%E6%B5%81%E9%80%9A%E5%B8%82%E5%80%BC&queryarea='
'http://www.iwencai.com/stockpick/cache?token=3ecda4f71d9daa85e5b040da069791dd&p=0&perpage=100'
"""
