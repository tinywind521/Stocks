# -*- coding:utf-8 -*-  
# author: Song Bo, Eagle, ZJU
# email: sbo@zju.edu.cn


def myAlign(string, length=0):
    if length == 0:
        return string
    slen = len(string)
    re = string
    if isinstance(string, str):
        placeholder = ' '
    else:
        placeholder = u'　'
    while slen < length:
        re += placeholder
        slen += 1
    return re


s1 = u'我是一个长句子，是的很长的句子。'
s2 = u'我是短句子'

print(myAlign(s1, 21) + myAlign(s2, 10))
print(myAlign(s2, 21) + myAlign(s1, 10))
