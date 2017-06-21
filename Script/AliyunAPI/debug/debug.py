def log(func):
    # func 参数传递的值就是 now方法
    def wrap(*args, **kw):

        # *args, **kw 方法接收任何形式的参数

        print('2016-05-10')
        return func(*args, **kw)  # 执行now方法
    return wrap


@log
def now():
    print('2016-05-11')

now()
