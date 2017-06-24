import operator

result = [1, 2, 3, 4, 5, 1, 2]
final = []
for temp1 in result:
    temp = True
    for temp2 in final:
        if operator.eq(temp1, temp2):
            temp = False
            print(temp1)
            print(temp2)
            break
        temp = True
    if temp:
        final.append(temp1)
print(final)

# def log(func):
#     # func 参数传递的值就是 now方法
#     def wrap(*args, **kw):
#
#         # *args, **kw 方法接收任何形式的参数
#
#         print('2016-05-10')
#         return func(*args, **kw)  # 执行now方法
#     return wrap
#
#
# @log
# def now():
#     print('2016-05-11')
#
# now()
