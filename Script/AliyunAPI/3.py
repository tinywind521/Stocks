def run(num):
    for i in range(0, num):
        yield i


print([i for i in run(10)])
