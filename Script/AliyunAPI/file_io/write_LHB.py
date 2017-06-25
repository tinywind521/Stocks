# import os
# import sys
# import ssl
# import json
#
# from file_io import txt
from functions import getValue

new_file = 'z:/test/LHB.csv'

# f = open(new_file, 'w')
# text = 'code, name, date, bs, no, yyname, yybuy, yysell\n'
# f.write(text)
# f.close()

# codelist = getValue.get_allCodelist()
codelist = ['002738', '002337', '000716', '000760', '000839', '000768', '000587', '000667',
            '300104', '300490', '300218', '300059', '000599', '002715', '002102', '300661',
            '000881', '300247', '300328', '300089', '600608', '600498', '600506', '600403',
            '600656', '600228', '600800', '600678', '600515', '600890', '600281', '603969',
            '600203', '600250', '600478', '600155', '603779', '600120', '600967']
"""
000716
000760
000839
000587
600608
600498
600506
600403
600656
600228
600800
600678
600515
600890
600281
600203
600250
600478
600155
600120
600967
"""
# 尚未抓取的部分
# depart = codelist.index(codelist1[-1])
# codelist = codelist[(depart + 1):]
for code in codelist:
    # code = '600215'
    print(code)
    code_text = ''
    if code[0] == '6':
        code_text = code + '.sh'
    elif code[0] == '0' or code[0] == '3':
        code_text = code + '.sz'

    tempStr = ''
    all_dict = getValue.get_CodeLHB(code)
    f = open(new_file, 'a+')
    for lhb_dict in all_dict:
        text = ''
        date = lhb_dict['date']
        date = date[0:4] + '/' + date[4:6] + '/' + date[6:8]
        tempStr = code_text + ',' + lhb_dict['name'] + ',' + date + ',' + lhb_dict['bs'] + ',' + lhb_dict['no'] + \
                  ',' + lhb_dict['yyname'] + ',' + lhb_dict['yybuy'] + ',' + lhb_dict['yysell'] + '\n'
        text = text + tempStr
        f.write(text)
    f.close()

# f.close()
