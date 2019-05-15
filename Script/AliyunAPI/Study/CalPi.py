import time
import random

n = 0
i = 0
while True:
    x = random.random()
    y = random.random()
    if x**2 + y**2 <= 1:
        i = i + 1
    n = n + 1
    pi = 4 * i / n
    print('\ri = {}, n = {}, pi = {}'.format(i, n, pi),end='')
    time.sleep(0.0000)
