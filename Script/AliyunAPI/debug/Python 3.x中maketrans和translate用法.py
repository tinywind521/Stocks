# 1. makestrans()用法
#
# 语法: str.maketrans(intab, outtab]);
#
# Python maketrans() 方法用于创建字符映射的转换表，对于接受两个参数的最简单的调用方式，
# 第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。
# 注：两个字符串的长度必须相同，为一一对应的关系。
#
# Python3.4已经没有string.maketrans()了，取而代之的是内建函数:
# bytearray.maketrans()、bytes.maketrans()、str.maketrans()
# """
#
# intab = "abcd"
# outtab = "1234"
# str_trantab = str.maketrans(intab,outtab)
#
# test_str = "csdn blog: http://blog.csdn.net/wirelessqa"
#
# print (test_str.translate(str_trantab)) # 3s4n 2log: http://2log.3s4n.net/wirelessq1
#
#
#
# """
#
# 2. translate() 用法
#
# 根据参数table给出的表(包含 256 个字符)转换字符串的字符, 要过滤掉的字符放到 del 参数中。
#
# 语法:
# str.translate(table[, deletechars]);
# bytes.translate(table[, delete])
# bytearray.translate(table[, delete])
#
# 若给出了delete参数，则将原来的bytes中的属于delete的字符删除，剩下的字符要按照table中给出的映射来进行映射
# """
#
# # 若table参数为None，则只删除不映射
# print(b'http://www.csdn.net/wirelessqa'.translate(None, b'ts'))   #b'hp://www.cdn.ne/wireleqa'
#
# # 若table参数不为NONE，则先删除再映射
# bytes_tabtrans = bytes.maketrans(b'abcdefghijklmnopqrstuvwxyz', b'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# print(b'http://www.csdn.net/wirelessqa'.translate(bytes_tabtrans, b'ts')) #b'HP://WWW.CDN.NE/WIRELEQA'
#
#
# """
# 3. 闭包: 它是个内层函数,由一个变量来指代,而这个变量对于外层包含它的函数来说是本地变量
#
# """
# def make_adder(addend):
#     def adder(augend):  #adder为内层函数
#         return augend + addend
#     return adder
#
# a = make_adder(1)  #产生一个闭包,addend为1,注意return的是adder
# b = make_adder(2)  #产生另一个闭包,addend为2,注意return的是adder
# print (a(100), b(100))  #a(100)就相当于adder(100),adden之前为1,因此返回100+1
#
# """
# 4. 对translate方法的简单封装,使用起来更加方便
# frm : intab
# to : outtab
# delete : 指定删除字符
# keep: 指定保留字符
# delete和keep有重叠时，delete优先
# """
# def my_translator(frm = b'', to = b'', delete = b'', keep = None):
#
#     if len(to) == 1:
#         to = to * len(frm) #如果to只有一个字符,将字符的数量跟frm相等,这样才能一一对应
#
#     #构建一个映射表
#     trans = bytes.maketrans(frm, to)
#
#     if keep is not None: #如果有保留字
#         allchars = bytes.maketrans(b'', b'')  # 获取空映射表的所有字符
#         keep = keep.translate(allchars, delete)  # 从keep中去除delete中包含的字符，即keep与delete有重合时，优先考虑delete
#         delete = allchars.translate(allchars, keep)  # delete为从全体字符中除去keep，即不在keep的都删掉
#
#
#     # 闭包
#     def my_translate(s):
#         return s.translate(trans, delete)
#
#     return my_translate
#
#
# # 测试my_tranlator
#
# # 只保留数字
# digits_only = my_translator(keep = b'0123456789')
# print(digits_only(b'http://www.csdn.net/wirelessqa 520520'))  #b'520520'
#
# # 删除所有数字
# no_digits = my_translator(delete = b'0123456789')
# print(no_digits(b'http://www.csdn.net/wirelessqa 520520'))  #b'http://www.csdn.net/wirelessqa '
#
# # 用*替换数字
# digits_to_hash = my_translator(frm = b'0123456789', to = b'*')
# print(digits_to_hash(b'http://www.csdn.net/wirelessqa 520520')) #b'http://www.csdn.net/wirelessqa ******'
#
# # delete与keep有重合时的情况
# trans = my_translator(delete = b'20', keep = b'0123456789')
# print(trans(b'http://www.csdn.net/wirelessqa 520520'))  # b'55'