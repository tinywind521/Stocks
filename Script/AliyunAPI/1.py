import time


def _int32(x):
    return int(0xFFFFFFFF & x)


class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        self.twist()
        y = self.mt[0]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        return _int32(y)

    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = y ^ self.mt[(i + 397) % 624] >> 1
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df


start = time.perf_counter()
for i in range(1000):
    # print(format(i))
    # a = MT19937(i)
    dur = time.perf_counter() - start
    print('\r{:04} / 1000 \t {:.3f}'.format(i, dur), end='')
    # print('\r{:04} / 1000 \t {:.3f} \t {}'.format(i,dur,a.extract_number()),end='')
    time.sleep(0.201)
