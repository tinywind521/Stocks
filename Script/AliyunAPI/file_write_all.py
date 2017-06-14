import os
import sys
import ssl
import json

from file_io import txt
#   from string import Template

root_path = 'Z:/Test/60F/'
new_path = 'z:/Test/'
new_file = new_path + '60F_All' + '.csv'
all_dict = {}
print(new_file)

#   template = Template('$code,$minute,$')

f = open(new_file, 'w')
text = 'id, minute, open, min, max, close, vol\n'
f.write(text)

for filename in os.listdir(root_path):
    all_dict = {}
    text = ''
    path = root_path + filename
#    print(path)
    s = txt.txt_read(path)
    try:
        all_dict = json.loads(s)
    except ValueError:
        pass

    showapi_res_body = all_dict['showapi_res_body']
    code = showapi_res_body['code']
    if code[0] == '6':
        code = code + '.sh'
    elif code[0] == '0' or code[0] == '3':
        code = code + '.sz'
    dataList = showapi_res_body['dataList']
#    print('minute, open, min, max, close, vol')
#    text = 'minute, open, min, max, close, vol\n'
    tempStr = ''
    for data_element in dataList:
        minute = data_element['minute']
        minute = minute[0:4] + '/' + minute[4:6] + '/' + minute[6:8] + '-' + minute[8:10] + ':' + minute[10:12]
#       data_element['minute'] = minute
#       print(minute)
#       minute = '201706051030'
        tempStr = code + ',' + minute + ',' + data_element['open'] + ',' + data_element['min'] + ',' \
                  + data_element['max'] + ',' + data_element['close'] + ',' \
                  + data_element['volumn'] + '\n' + tempStr
#        break

    text = text + tempStr
    f.write(text)

f.close()
#    break
