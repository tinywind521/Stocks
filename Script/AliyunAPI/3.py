a = 1
b = input('input:')
try:
    print(a / b)
except (ZeroDivisionError, TypeError):
    pass
