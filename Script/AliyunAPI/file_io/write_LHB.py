# import os
# import sys
# import ssl
# import json
#
# from file_io import txt
from functions import getValue

new_file = 'z:/test/LHB.csv'
code = '600215'
code_text = ''


f = open(new_file, 'w')
text = 'code, name, date, bs, no, yyname, yybuy, yysell\n'
f.write(text)
if code[0] == '6':
    code_text = code + '.sh'
elif code[0] == '0' or code[0] == '3':
    code_text = code + '.sz'

tempStr = ''
all_dict = getValue.get_CodeLHB(code)
for lhb_dict in all_dict:
    text = ''
    date = lhb_dict['date']
    date = date[0:4] + '/' + date[4:6] + '/' + date[6:8]
    tempStr = code_text + ',' + lhb_dict['name'] + ',' + date + ',' + lhb_dict['bs'] + ',' + lhb_dict['no'] + \
              ',' + lhb_dict['yyname'] + ',' + lhb_dict['yybuy'] + ',' + lhb_dict['yysell'] + '\n'
    text = text + tempStr
    f.write(text)

f.close()
