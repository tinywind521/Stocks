import time

start = time.perf_counter()
for i in range(1000):
    # print(format(i))
    dur = time.perf_counter() - start
    print('\r{:04} / 1000 \t {:.3f}'.format(i,dur),end='')
    time.sleep(0.201)