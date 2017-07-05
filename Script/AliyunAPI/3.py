from http_api import sina_api
from functions import getValue
import os


# codeList = getValue.get_availableCodeList()
# codeList = codeList[0:500]
# finalList = []
# for code in codeList:
#     if code[0] == '6':
#         finalList.append('sh' + code)
#     elif code[0] == '0' or code[0] == '3':
#         finalList.append('sz' + code)
# s = sina_api.timeline(finalList)
# print(s)
# t = s.count('var hq_str')
class hehe:
    def __init__(self, temp):
        self._list_l = []
        self._list_r = []
        self._seq_l = []
        self._seq_r = []

        s = 1
        judge = 1
        if s == 1:
            if judge:
                self._list_l.append(temp)
            else:
                s = 2
                self._seq_l.append(self._list_l[:])
                self._list_r.clear()
                self._list_r.append(temp)
        elif s == 2:
            if not judge:
                self._list_r.append(temp)
            else:
                s = 1
                self._seq_r.append(self._list_r[:])
                self._list_l.clear()
                self._list_l.append(temp)

        if s:
            pass

