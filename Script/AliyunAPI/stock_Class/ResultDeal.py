class ResultDeal:
    def __init__(self, firstValue=None):
        self._result = firstValue
        self._ArrayResult = []
        self._DictResult = {}
        self._title = None

    """旧结构使用，暂时不修改"""
    def setResultAppend(self, key, tempArg):
        self._result[key].append(tempArg)

    def getResultValue(self):
        return self._result

    """数组处理"""
    def setResultArrayAppend(self, tempArg):
        self._ArrayResult.append(tempArg)

    def setResultArrayExtend(self, tempArg):
        self._ArrayResult.extend(tempArg)

    def getArrayResultValue(self):
        return self._ArrayResult

    def resetArrayResultValue(self):
        self._ArrayResult = []

    """字典处理"""
    def setResultDictAppend(self, key, tempArg):
        self._DictResult[key].append(tempArg)

    def getDictResultValue(self):
        return self._DictResult

    def resetDictResultValue(self):
        self._DictResult = {}

    """其他处理"""
    def setTitle(self, title):
        if self._title:
            pass
        else:
            self._title = title

    def getTitle(self):
        return self._title
