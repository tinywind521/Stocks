import pandas as pd

def getPeak(data, halfWindow=2, MAkernal=2):
    print(data)
    data['maxValue'] = pd.Series(data.apply(lambda x: max(x.open, x.close), axis=1), name='max')
    data.to_csv('d:/data/' + code + '.csv')
    print(temp)
    pass


if __name__ == '__main__':
    from multiprocessing.dummy import Pool as ThreadPool
    from Dino.DataSource.httpAPI import DataSourceQQ as QQ
    from Dino.DataSource.httpAPI import DailyQQMul as QQMul
    from Dino.DataSource.httpAPI import DataTuShare as Tu
    from Dino.DataSource import filter

    import time
    import sys

    if __name__ == '__main__':
        debug = 0
        print(time.strftime("%H:%M:%S", time.localtime()))
        code = '000004'
        data = QQMul(code)
        data.updateDailyKLine()
        data.updateHourKLine()
        temp = data.kLine60F
        getPeak(temp)
        print()
        print(time.strftime("%H:%M:%S", time.localtime()))
    pass
