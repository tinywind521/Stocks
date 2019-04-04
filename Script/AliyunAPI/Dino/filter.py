from multiprocessing.dummy import Pool as ThreadPool
from Dino.DataSource.httpAPI import DataSourceQQ as QQ
from Dino.DataSource.httpAPI import DataTuShare as Tu

import time


class Filter:
    """
    筛选过滤器
    """
    def __init__(self):
        pass
        # self.code = code
'''
length = len(codeList)
r = ResultDeal(result)
for i in range(0, length, PoolLength):
    realList = codeList[i:i + PoolLength]
    realLength = len(realList)
    function.view_bar(i + realLength, length)
    pool = ThreadPool(realLength)
    objTemp = [{'codeArg': k, 'objResult': r, 'ref_List': ref_List} for k in realList]
    pool.map(function.calDayStatus, objTemp)
    pool.close()
    pool.join()
result = r.getResultValue()
'''

if __name__ == '__main__':
    debug = 0
    code = '603963'
    data = Tu()
    stockList = data.getList()
    print(stockList)
    if not debug:
        data.setCode(code)
        data.getDailyKLine()
        data.updateDailyKLine()
        while True:
            try:
                data.dailyKline.to_csv('d:/' + code + '.csv')
                break
            except PermissionError:
                input('The file is open...please close it!!!')
    if debug:
        j = 0
        for code in stockList:
            data.setCode(code)
            # print(code)
            while True:
                # noinspection PyBroadException
                try:
                    data.getDailyKLine()
                    # data.updateDailyKLine()
                    break
                except Exception:
                    print(code, 'time sleep...')
                    time.sleep(60)
            data.updateDailyKLine()
            try:
                if len(data.dailyKline['close']):
                    print(code, 'mid20:\t', data.dailyKline['mid20'][0], '\trunning...')
                else:
                    print(code, 'no data!!!')
            except ValueError or KeyError or IndexError:
                pass
            try:
                if data.dailyKline.head(1)['limit'][0] == 1:
                    # {col: data.dailyKline[col].tolist() for col in data.dailyKline.columns}
                    print(dict(data.dailyKline[0:1]['ts_code'])[0], 'Limited!!!')
                    j += 1
            except:
                pass
        print(j)

    if code is not None:
        test = QQ(code)
        test.updateKLine()
        # test = DataSource_iFeng(code)
        pass
    else:
        raise ValueError
    print(test.timeLine5DaysAllinOne)
    test.timeLine5DaysAllinOne.to_csv('D:/min.csv')
    b = test.kLine60F
    b.to_csv('D:/hour.csv')
    print(b)
    # print(test.timeLine)
    # for i in test.timeLine5DaysAllinOne:
    #     print(i)
    # for i in test.timeLine5DaysDaily:
    #     print(i)
    # for i in test.kLine60F:
    #     print(i)
    # print(test.kLineDay['record'])