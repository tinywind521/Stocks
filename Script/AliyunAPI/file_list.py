import os
import sys
import ssl
import json

from file_io import txt

root_path = 'Z:/Test/60F/'
new_path = 'z:/Test/Result/'

for filename in os.listdir(root_path):
    all_dict = {}
    path = root_path + filename
#    print(path)
    s = txt.txt_read(path)
    try:
        all_dict = json.loads(s)
    except:ValueError
    pass

    showapi_res_body = all_dict['showapi_res_body']
    code = showapi_res_body['code']
    dataList = showapi_res_body['dataList']
#    print('minute, open, min, max, close, vol')
    text = 'minute, open, min, max, close, vol\n'
    tempStr = ''
    for data_element in dataList:
        minute = data_element['minute']
        minute = minute[0:4] + '/' + minute[4:6] + '/' + minute[6:8] + '-' + minute[8:10] + ':' + minute[10:12]
#       print(minute)
#       minute = '201706051030'
        tempStr = minute + ',' + data_element['open'] + ',' + data_element['min'] + ','\
                  + data_element['max'] + ',' + data_element['close'] + ','\
                  + data_element['volumn'] + '\n' + tempStr
#        break
#    print(tempStr)
    text = text + tempStr
    new_file = new_path + code + '.csv'
    print(new_file)
    txt.txt_write(text, new_file)
#    break
