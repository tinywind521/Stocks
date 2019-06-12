import time
import random

i = 0
for n in range(1, 9999999999):
    x = random.random()
    y = random.random()
    if x**2 + y**2 <= 1:
        i = i + 1
    pi = 4 * i / n
    print(n)
print('\rpi = {}\tn = {}'.format(pi, n),end='')
    # time.sleep(0.0000)
