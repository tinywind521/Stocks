from bs4 import BeautifulSoup
import urllib.request
import requests

url = "http://finance.qq.com/gdyw.htm"

# 使用urllib.request的代码：
html = urllib.request.urlopen(url).read()
html = html.decode('gb2312', errors='ignore')
soup1 = BeautifulSoup(html, 'lxml')
lfls1 = str(soup1).split('<!-- 左侧列表 -->', 2)

# 使用requests的代码：
response = requests.get(url)
soup2 = BeautifulSoup(response.text, 'lxml')
lfls2 = str(soup2).split('<!-- 左侧列表 -->', 2)

print(lfls1[1][:500])
print('='*70)
print(lfls2[1][:500])
