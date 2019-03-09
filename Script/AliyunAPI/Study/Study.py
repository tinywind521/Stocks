from Dino.DataSource.httpAPI import DataSourceQQ

import sys

test = DataSourceQQ('000514')
print(test.timeLine)
print(test.timeLine5Days)
print(test.kLine60F)
print(test.kLineDay)

def view_bar(num, total, codeIn=''):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    r = '\r[%s%s] %2.2f%% %d/%d %s' % ("|"*flow, " "*(100-flow), rate_num, num, total, codeIn,)
    sys.stdout.write(r)
    sys.stdout.flush()