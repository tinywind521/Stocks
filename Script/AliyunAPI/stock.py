from functions import getValue


class Stock:
    """
    stock 类的测试版
    code: 代码
    ref_list: 包含timetype、beginDay、appcode等在内其他参数字典
    """
    def __init__(self, code, ref_List):
        if ref_List is None:
            ref_List = {'KtimeType': '60/day',
                        'KbeginDay': '20170101',
                        'KgetLength': 10,
                        'TdayLength': 1,
                        'TdataLength': 242,
                        'appcode': 'c7689f18e1484e9faec07122cc0b5f9e'}
        self.code = code
        self._ref_list = ref_List
        self.Kvalue = None
        self.Tvalue = None
        # self.value = self.get_KValue()


    def get_KLine(self):
        """
        计算各级别的K线
        :return:
        """
        try:
            if self._ref_list['KtimeType'] == '60':
                self.Kvalue = getValue.get_60F(self.code, self._ref_list['KbeginDay'], self._ref_list['KgetLength'])
            elif self._ref_list['KtimeType'] == 'day':
                self.Kvalue = getValue.get_dayK_Line(self.code, self._ref_list['KbeginDay'], self._ref_list['KgetLength'])
        except ValueError:
            pass


    def set_KbeginDay(self, beginDay='20170101'):
        self._ref_list['KbeginDay'] = beginDay


    def set_KtimeType(self, timetype='60'):
        self._ref_list['KtimeType'] = timetype


    def set_KgetLength(self, getLength=10):
        self._ref_list['KgetLength'] = getLength


    def get_KtimeType(self):
        return self._ref_list['KtimeType']


    def set_Clear(self):
        """
        清空K线序列
        :return:
        """
        self.Kvalue = None


    def set_Refresh(self):
        """
        刷新K线序列
        :return:
        """
        self.set_Clear()
        self.get_KValue()


    def get_KValue(self):
        """
        该函数作用便于多次读取K线数据
        但不需要多次联网
        :return:
        """
        if self.Kvalue is None:
            # print('Link Web!')
            self.get_KLine()
            return self.Kvalue
        else:
            return self.Kvalue


    def boll_mid(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self.get_KLine()
        bollmid = self.Kvalue[-1-n]['mid']
        return bollmid


    def boll_upper(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self.get_KLine()
        bollupper = self.Kvalue[-1-n]['upper']
        return bollupper


    def boll_lower(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self.get_KLine()
        bolllower = self.Kvalue[-1-n]['lower']
        return bolllower


    def get_TLine(self, code, ref_List):
        if ref_List is None:
            ref_List = {'dayLength': 5,
                        'dataLength': 242,
                        'appcode': 'c7689f18e1484e9faec07122cc0b5f9e'}
        self.code = code
        self._ref_list = ref_List
        self.value = None
