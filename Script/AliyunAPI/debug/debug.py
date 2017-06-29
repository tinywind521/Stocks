a = [1, 2, 3]
a[1:1] = [0, 0, 0]
try:
    b = a.index(4)
except ValueError:
    b = None
a.append(4)
print(a)
print(b)
