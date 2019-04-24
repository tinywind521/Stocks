from multiprocessing.dummy import Pool as ThreadPool
from Dino.DataSource.httpAPI import DataSourceQQ as QQ
from Dino.DataSource.httpAPI import DailyQQMul as QQMul
from Dino.DataSource.httpAPI import DataTuShare as Tu
from Dino.DataSource.httpAPI import DataTuShareMul as TuMul

import time
import sys

def getCodeListAndColList():
    value = {'codeList':[], 'colList':[]}
    data = Tu()
    codeList = data.getList()
    print('List get!')
    data.setCode(codeList[0])
    data.getDailyKLine()
    data.updateDailyKLine()
    colList = data.colList
    value['codeList'] = codeList
    value['colList'] = colList
    return value

def view_bar(num, total, codeIn=''):
    rate = num / total
    rate_num = rate * 100
    flow = int(rate_num)
    r = '\r[%s%s] %2.2f%% %d/%d %s' % ("|"*flow, " "*(100-flow), rate_num, num, total, codeIn,)
    sys.stdout.write(r)
    sys.stdout.flush()

def dailySingleDataCapture(objTemp):
    """
    多线程处理
    DataTuShareMul
    :param codeTemp: objTemp = [{'code': k, 'obj': self.tu} for k in realList]
    :return:
    """
    code = objTemp['code']
    # print(code)
    data = QQMul(code)
    # obj.updateDailyKLine(colList, code)
    while True:
        try:
            data.updateDailyKLine()
            break
        except ValueError:
            print(code, 'time sleep...')
            time.sleep(60)


def dailySingleDataCaptureTu(objTemp):
    """
    多线程处理
    DataTuShareMul
    :param codeTemp: objTemp = [{'code': k, 'obj': self.tu} for k in realList]
    :return:
    """
    obj = objTemp['obj']
    code = objTemp['code']
    colList = objTemp['colList']
    try:
        code = obj.setCode(code)
    except:
        return
    # obj.updateDailyKLine(colList, code)
    # print(code)
    while True:
        try:
            obj.updateDailyKLine(colList, code)
            break
        except ValueError:
            print(code, 'time sleep...')
            time.sleep(60)



class StockFilter:
    """
    筛选过滤器
    """
    def __init__(self, codeList, colList):
        self.codeList = codeList
        self.colList = colList
        self.code = None
        # self.tu = TuMul()
        # self.obj = QQ()
        """
        多线程设定
        """
        self.poolLength = 20
        # self.qq = QQ(self.code)
        pass
        # self.code = code

    def getDailyDataMul(self):
        length = len(self.codeList)
        for i in range(0, length, self.poolLength):
            realList = self.codeList[i:i + self.poolLength]
            # print(realList)
            realLength = len(realList)
            view_bar(i + realLength, length)
            pool = ThreadPool(realLength)
            # objTemp = [{'code': k, 'colList': self.colList, 'obj': self.obj} for k in realList]
            objTemp = [{'code': k} for k in realList]
            # print(objTemp)
            pool.map(dailySingleDataCapture, objTemp)
            pool.close()
            pool.join()

    def getDailyData(self):
        pass


if __name__ == '__main__':
    debug = 0
    value = getCodeListAndColList()
    print(value['codeList'])
    print(value['colList'])
    data = StockFilter(value['codeList'], value['colList'])
    data.getDailyDataMul()