def ss(string=[]):
    for s in string:
        print(s)
    return None
try:
    d = input('Input Reference: ')
    dd = list(d)
    print(dd)
    ss(dd)
except:
    print('Ref Error!')