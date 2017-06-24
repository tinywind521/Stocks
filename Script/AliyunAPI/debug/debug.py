s = {'code': '300668', 'name': 'N杰恩', 'bs': 'B', 'no': '3', 'date': '20170619', 'yyname': '华宝证券有限责任公司成都天泰路证券营业部', 'yybuy': '2510.0000', 'yysell': '0.0000'}

l = [{'code': '300668', 'name': 'N杰恩', 'bs': 'B', 'no': '1', 'date': '20170619', 'yyname': '东海证券股份有限公司常州通江中路证券营业部', 'yybuy': '118131.0000', 'yysell': '0.0000'},
     {'code': '300668', 'name': 'N杰恩', 'bs': 'B', 'no': '2', 'date': '20170619', 'yyname': '国信证券股份有限公司深圳振华路证券营业部', 'yybuy': '5522.0000', 'yysell': '0.0000'},
     {'code': '300668', 'name': 'N杰恩', 'bs': 'S', 'no': '3', 'date': '20170619', 'yyname': '华宝证券有限责任公司成都天泰路证券营业部', 'yybuy': '2510.0000', 'yysell': '0.0000'}]

t = l.index(s)
print(t)

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
