import math

from functions import getValue, function


class ResultDeal:
    def __init__(self, firstValue):
        self._result = firstValue

    def setResultAppend(self, key, tempArg):
        self._result[key].append(tempArg)

    def getResultValue(self):
        return self._result


class Stock:
    """
    stock 类的测试版
    code: 代码
    ref_list: 包含timetype、beginDay、appcode等在内其他参数字典
    开发者：Q0233
    最后更新：未完成
    注意：分时数据是逆序，K线数据是顺序。
    """

    def __init__(self, code, ref_List):
        if ref_List is None:
            ref_List = {'KtimeType': '60/day',
                        'KbeginDay': '20170101',
                        'KallLength': 160,
                        'KgetLength': 10,
                        'TdayLength': 5,
                        'TgetLength': 1,
                        'appcode': 'c7689f18e1484e9faec07122cc0b5f9e',
                        'showapi_code': '6a09e5fe3e724252b35d571a0b715baa',
                        'need144': 0,
                        }
        self.code = code
        self._ref_list = ref_List
        self.Kvalue = None
        self.Tvalue = None
        # self.value = self.get_KValue()
        self.Kstatus = {'涨幅': 0, '开收': 0, '量能': 0, '上针': 0, '下针': 0,
                        '布林': 0, '55布林': 0, '144布林': 0, '轨距': 0, '层级': '',
                        '趋势': None, '底部': None,
                        '平台': '', '序号': 0, '预留': '', '备用': ''}

    def get_ref_List(self):
        return self._ref_list

    """
    无情的分割线
    下面是获取基本K线的函数方法
    """

    def _get_KLine(self):
        """
        获取各级别的K线
        :return: Error return None
        """
        try:
            if self._ref_list['KtimeType'] == '60':
                self.Kvalue = getValue.get_60F_qtimq(self.code, self._ref_list['KallLength'],
                                                     self._ref_list['KgetLength'])
                # self.Kvalue = getValue.get_60F_qtimq(self.code, self._ref_list['KallLength'],
                #                                      self._ref_list['KgetLength'])[0:-4]
                # print(self.Kvalue[-1])
            elif self._ref_list['KtimeType'] == 'day':
                self.Kvalue = getValue.get_dayK_qtimq(self.code, self._ref_list['KallLength'],
                                                      self._ref_list['KgetLength'])
                # self.Kvalue = getValue.get_dayK_qtimq(self.code, self._ref_list['KallLength'],
                #                                       self._ref_list['KgetLength'])[0:-1]
                # print(self.Kvalue[-1])
        except ValueError:
            try:
                if self._ref_list['KtimeType'] == '60':
                    self.Kvalue = getValue.get_60F_qtimq(self.code, self._ref_list['KallLength'],
                                                         self._ref_list['KgetLength'])
                elif self._ref_list['KtimeType'] == 'day':
                    self.Kvalue = getValue.get_dayK_qtimq(self.code, self._ref_list['KallLength'],
                                                          self._ref_list['KgetLength'])
            except ValueError:
                self.Kvalue = None

    def get_KValue(self):
        """
        该函数作用便于多次读取K线数据
        但不需要多次联网
        :return:
        """
        if self.Kvalue is None:
            # print('Link Web!')
            self._get_KLine()
            return self.Kvalue
        else:
            return self.Kvalue

    def set_KbeginDay(self, KbeginDay='20170101'):
        self._ref_list['KbeginDay'] = KbeginDay

    def set_KtimeType(self, Ktimetype='60'):
        self._ref_list['KtimeType'] = Ktimetype

    def set_KgetLength(self, KgetLength=10):
        self._ref_list['KgetLength'] = KgetLength

    def get_KbeginDay(self):
        return self._ref_list['KbeginDay']

    def get_KtimeType(self):
        return self._ref_list['KtimeType']

    def get_KgetLength(self):
        return self._ref_list['KgetLength']

    def set_KClear(self):
        """
        清空K线序列
        :return:
        """
        self.Kvalue = None
        self.Kstatus = None

    def set_KRefresh(self):
        """
        刷新K线序列
        :return:
        """
        self.set_KClear()
        self.get_KValue()

    """
    无情的分割线
    下面是分时的函数方法
    """

    def _get_TLine(self):
        """
        获取分时线
        :return: Error return None
        """
        try:
            self.Tvalue = getValue.get_timeLine(self.code,
                                                self._ref_list['TdayLength'])
        except ValueError:
            self.Tvalue = None

    def get_TValue(self):
        """
        该函数作用便于多次读取分时数据
        但不需要多次联网
        :return:
        """
        if self.Tvalue is None:
            self._get_TLine()
            # print(self._ref_list)
            self.Tvalue = self.Tvalue[0: self._ref_list['TgetLength']]
            return self.Tvalue
        else:
            if len(self.Tvalue) < self._ref_list['TgetLength']:
                self._get_TLine()
                self.Tvalue = self.Tvalue[0: self._ref_list['TgetLength']]
            else:
                self.Tvalue = self.Tvalue[0: self._ref_list['TgetLength']]
            return self.Tvalue

    def set_TdayLength(self, TdayLength=5):
        self._ref_list['TdayLength'] = TdayLength

    def set_TgetLength(self, TgetLength=1):
        if TgetLength > self._ref_list['TdayLength']:
            self._ref_list['TdayLength'] = self._ref_list['TdayLength']
        else:
            self._ref_list['TgetLength'] = TgetLength

    def get_TdayLength(self):
        return self._ref_list['TdayLength']

    def get_TgetLength(self):
        return self._ref_list['TgetLength']

    def set_TClear(self):
        """
        清空分时序列
        :return:
        """
        self.Tvalue = None

    def set_TRefresh(self):
        """
        刷新分时序列
        :return:
        """
        self.set_TClear()
        self.get_TValue()

    """
    无情的分割线
    下面是布林的函数方法
    """

    def boll_mid(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self._get_KLine()
        bollmid = self.Kvalue[-1 - n]['mid']
        return bollmid

    def boll_upper(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self._get_KLine()
        bollupper = self.Kvalue[-1 - n]['upper']
        return bollupper

    def boll_lower(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self._get_KLine()
        bolllower = self.Kvalue[-1 - n]['lower']
        return bolllower

    def boll_position(self, boll_Kvalue):
        """
        判断K线所处布林位置。
        由于目前暂无法定义一线穿多轨的情况，暂时以收盘价位置为准。
        结果分类：
        +4：高于上轨
        +3：等于上轨
        +2：中上轨上部空间
        +1：中上轨下部空间
        0：等于中轨
        -1：中下轨上部空间
        -2：中下轨下部空间
        -3：等于下轨
        -4：低于下轨
        :return:
        """

        self.Kstatus['布林'] = 0

        """中上轨上下分层标准"""
        upper_mid = (boll_Kvalue['upper'] + boll_Kvalue['mid']) / 2
        """中下轨上下分层标准"""
        lower_mid = (boll_Kvalue['lower'] + boll_Kvalue['mid']) / 2

        if boll_Kvalue['close'] > boll_Kvalue['upper']:
            "+4：高于上轨"
            self.Kstatus['布林'] = +4
        elif boll_Kvalue['close'] == boll_Kvalue['upper']:
            "+3：等于上轨"
            self.Kstatus['布林'] = +3
        elif boll_Kvalue['close'] > upper_mid:
            "+2：中上轨上部空间"
            self.Kstatus['布林'] = +2
        elif boll_Kvalue['close'] > boll_Kvalue['mid']:
            "+1：中上轨下部空间"
            self.Kstatus['布林'] = +1
        elif boll_Kvalue['close'] == boll_Kvalue['mid']:
            "0：等于中轨"
            self.Kstatus['布林'] = 0
        elif boll_Kvalue['close'] > lower_mid:
            "-1：中下轨上部空间"
            self.Kstatus['布林'] = -1
        elif boll_Kvalue['close'] > boll_Kvalue['lower']:
            "-2：中下轨下部空间"
            self.Kstatus['布林'] = -2
        elif boll_Kvalue['close'] == boll_Kvalue['lower']:
            "-3：等于下轨"
            self.Kstatus['布林'] = -3
        elif boll_Kvalue['close'] < boll_Kvalue['lower']:
            "-4：低于下轨"
            self.Kstatus['布林'] = -4
        else:
            pass

        self.Kstatus['144布林'] = 0

        """中上轨上下分层标准"""
        upper144_mid144 = (boll_Kvalue['upper144'] + boll_Kvalue['mid144']) / 2
        """中下轨上下分层标准"""
        lower144_mid144 = (boll_Kvalue['lower144'] + boll_Kvalue['mid144']) / 2

        if boll_Kvalue['close'] > boll_Kvalue['upper144']:
            "+4：高于上轨"
            self.Kstatus['144布林'] = +4
        elif boll_Kvalue['close'] == boll_Kvalue['upper144']:
            "+3：等于上轨"
            self.Kstatus['144布林'] = +3
        elif boll_Kvalue['close'] > upper144_mid144:
            "+2：中上轨上部空间"
            self.Kstatus['144布林'] = +2
        elif boll_Kvalue['close'] > boll_Kvalue['mid144']:
            "+1：中上轨下部空间"
            self.Kstatus['144布林'] = +1
        elif boll_Kvalue['close'] == boll_Kvalue['mid144']:
            "0：等于中轨"
            self.Kstatus['144布林'] = 0
        elif boll_Kvalue['close'] > lower144_mid144:
            "-1：中下轨上部空间"
            self.Kstatus['144布林'] = -1
        elif boll_Kvalue['close'] > boll_Kvalue['lower144']:
            "-2：中下轨下部空间"
            self.Kstatus['144布林'] = -2
        elif boll_Kvalue['close'] == boll_Kvalue['lower144']:
            "-3：等于下轨"
            self.Kstatus['144布林'] = -3
        elif boll_Kvalue['close'] < boll_Kvalue['lower144']:
            "-4：低于下轨"
            self.Kstatus['144布林'] = -4
        else:
            pass
        # print(self.Kstatus)

    """
    华丽的分割线
    下面是获取K线参数的函数方法
    """

    def update_Kstatus(self):
        if self.Kvalue:
            # print(self.Kvalue)
            i = 0
            for _Kvalue in self.Kvalue:
                # print(_Kvalue)
                self.update_Kpara(_Kvalue)
                _Kvalue.update(self.Kstatus)
                self.Kvalue[i] = _Kvalue
                i += 1

    # def clear_Kstatus(self):
    #     self.Kstatus = None


    def update_Kpara(self, _Kvalue):
        """
        按照K线的涨幅、开盘收盘涨幅、收针判断、布林位置、结合收针的量能 归类 量化
        zf：涨幅
        ks：收盘对应开盘的涨幅（基准为昨收）
        sz：上针幅度（基准为振幅）
        xz：下针幅度（基准为振幅）
        gj：布林上下轨距（基准为昨收）

        :return:
        """
        try:
            if round(_Kvalue['lastclose'] * 1.10, 2) == _Kvalue['close']:
                zf = 10.00
            elif round(_Kvalue['lastclose'] * 0.90, 2) == _Kvalue['close']:
                zf = -10.00
            else:
                zf = 100.00 * (_Kvalue['close'] - _Kvalue['lastclose']) / _Kvalue['lastclose']
            ks = 100.00 * (_Kvalue['close'] - _Kvalue['open'] + 0.001) / _Kvalue['lastclose']
            gj = 100.00 * (_Kvalue['upper'] - _Kvalue['lower']) / _Kvalue['mid']
        except ZeroDivisionError or KeyError:
            self.Kstatus['涨幅'] = 0
            self.Kstatus['开收'] = 0
            self.Kstatus['上针'] = 0.00
            self.Kstatus['下针'] = 0.00
            self.Kstatus['轨距'] = 0.00
            self.Kstatus['布林'] = 0
            self.Kstatus['144布林'] = 0
        else:
            self.Kstatus['涨幅'] = math.floor(zf)
            self.Kstatus['开收'] = math.floor(ks)
            self.Kstatus['轨距'] = math.floor(gj)
            self.boll_position(_Kvalue)
            try:
                high = max(_Kvalue['open'], _Kvalue['close'])
                low = min(_Kvalue['open'], _Kvalue['close'])
                full = _Kvalue['max'] - _Kvalue['min']
                sz = 100.00 * (_Kvalue['max'] - high) / full
                xz = 100.00 * (low - _Kvalue['min']) / full
            except ZeroDivisionError or KeyError:
                self.Kstatus['上针'] = 0.00
                self.Kstatus['下针'] = 0.00
            else:
                self.Kstatus['上针'] = math.floor(sz)
                self.Kstatus['下针'] = math.floor(xz)


class Yline:
    """
    连续阴线/阳线 类的测试版
    Kvalue: K线
    para: 待定参数
    开发者：Q0233
    最后更新：未完成
    注意：分时数据是逆序，K线数据是顺序。

    目标：
    # [
    #     { [ {连续K线1参数 }, {连续K线2参数}, {连续K线3参数}...], {第1组连续K线的组参数} },
    #     { [ {连续K线1参数 }, {连续K线2参数}, {连续K线3参数}...], {第2组连续K线的组参数} },
    #     ...
    #     { [ {连续K线1参数 }, {连续K线2参数}, {连续K线3参数}...], {第i组连续K线的组参数} },
    # ]

    层级差合并地量形成强支撑（首次力度极强），如果合并趋势线或者中轨等一般支撑，效果明显！！！
    （连续）层级差的趋势逆转、趋势加强和趋势释放。
    单根K线目前量化的参数如下：
        1、单日参数：4价，量能，涨幅，布林参数， 还增加了布林位置和结合收针的量能
        2、两日参数：缩量/放量的程度（相对量能比值），缺口宽度
        3、多日参数：是否是层级差，地量或者峰值量
    注意反向层级差
    不要怂，就是干！
    """

    def __init__(self, Kvalue, para):
        """
        初始化
        :param Kvalue:
        :param para:
        """
        """统计阴线和阳线数量"""
        self._bull_length = 0
        self._bear_length = 0
        self._all_length = 0

        """计算层级差用到的序列变量"""
        self._list_bull = []
        self._list_bear = []
        self._seq_bull = []
        self._seq_bear = []
        self._seq = []
        self._levelList = []
        self._head = []
        self._rear = []
        self._lastLevelName = None
        self._lastLevelResult = 0.00
        self._fallTimes = 0
        self._raised = None
        self._highestLevel = -10
        self._highestPrice = 0

        self.levelTimes = None
        self._lastFirstK = None
        self._lastSecondK = None

        """计算结果和形态结果"""
        self.bull_por = 0.00
        self.patternResult = None
        self.maxChange = None

        """过程参数"""
        self._paraList = ['序号', 'time', 'open', 'min', 'max', 'close', 'lastclose', 'volumn',
                          'upper', 'mid', 'lower', 'upper144', 'mid144', 'lower144',
                          '涨幅', '开收', '量能', '上针',
                          '下针', '布林', '144布林', '底部', '轨距', '层级', '趋势', '平台']

        """minVol 近期地量"""
        self.minVol = 0
        self._YY_VolumnList = None
        self._setPrint = 0
        if para is None:
            para = {
                '收针对量能的影响系数': 0.75,
                '评分初值': 100,
                '以下是层级差中用到的系数': 0,

            }
            self._para = para
        if Kvalue is None or len(Kvalue) == 0:
            # Kvalue = Stock.get_KValue()
            raise ValueError('input Kvalue is None!')
        else:
            self._para = para
            self.Index = None
            self.status = self._para['评分初值']

            """Index 为量化指标"""
            self._cal_index(Kvalue)


            # [{[{}], {}}]
            # { [ {连续K线1参数 }, {连续K线2参数}, {连续K线3参数}...], {第2组连续K线的组参数} },

    def get_bull_length(self):
        return self._bull_length

    def get_bear_length(self):
        return self._bear_length

    def get_all_length(self):
        return self._all_length

    def get_para(self):
        return self._para

    """
    获取阳线层级总列表
    """
    def get_seq_bull(self):
        return self._seq_bull

    """
    获取阴线层级总列表
    """
    def get_seq_bear(self):
        return self._seq_bear

    """
    获取阴阳层级总列表
    """
    def get_seq_all(self):
        return self._seq

    """
    获取层级列表
    """
    def get_levelList(self):
        return self._levelList

    """
    刷新K线量化指标
    """
    def refresh_index(self, Kvalue):
        """
        刷新K线量化指标
        :param Kvalue:
        :return:
        """
        self._cal_index(Kvalue)

    """
    先用0/1，建立连乘评分机制，
    根据后续使用情况，0/1 --> 0.90~1.10的连乘机制
    """
    def _index_cont_bear(self):
        """
        把连续阴线分成前面n根和最后一根，判断最后一根
        k倍率
        条件：
            1、不是最大量能；
            2、小于前期阴线平均值；
        :return:
        """
        beginStatus = self.status
        lastBear = self._head.pop(-1)
        # print(lastBear)
        preBearList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
        # print(preBearList)
        # """ 满足2必然满足1 """
        # if lastBear['量能'] > k * (sum(preBearList) / len(preBearList)):
        #     self.status *= 0
        # else:
        #     self.status *= 1
        """连续阴线缩量占比系数"""
        k = 0.10
        try:
            self.status *= k * ((sum(preBearList) / len(preBearList)) / lastBear['量能'] - 1) + 1
        except ZeroDivisionError:
            self.status *= 1
        self._lastLevelResult = self.status / beginStatus

    def _index_rise_level(self):
        """
        上升层级差，中间必有阳线，阳线放量（两侧阴线最大值的k倍率）

        注意：
        初版暂时没考虑涨停的情况，观察一下效果，后续修改

        :return:
        """
        """上升层级差缩量占比系数"""
        """中间阳线"""
        k1 = 0.125
        """前后阴线"""
        k2 = 0.10

        beginStatus = self.status
        headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
        # print(self._head)
        # print(headVolList)
        rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
        # print(self._rear)
        # print(rearVolList
        midBullList = self._YY_VolumnList[(self._head[-1]['序号'] + 1):self._rear[0]['序号']]
        # if k * self._YY_VolumnList[self._rear[0]['序号']] > max(midBullList):
        #     self.status *= 0
        # else:
        #     self.status *= 1
        try:
            if self._YY_VolumnList[self._rear[0]['序号']] != 0:
                self.status *= k1 * (max(midBullList) / self._YY_VolumnList[self._rear[0]['序号']] - 1) + 1
            else:
                self.status *= 1
        except ValueError or ZeroDivisionError:
            self.status *= 1
        try:
            if len(headVolList) != 0 and len(rearVolList) != 0 and sum(rearVolList) != 0:
                self.status *= k2 * ((sum(headVolList) / len(headVolList)) / (sum(rearVolList) / len(rearVolList)) - 1)\
                               + 1
            else:
                self.status *= 1
        except ValueError or ZeroDivisionError:
            self.status *= 1
        self._lastLevelResult = self.status / beginStatus

    def _index_fall_level(self):
        """
        下降层级差，
        1、序号连续：
            不是连续的最后一根，就先不判断，如果是连续阴线的最后一根，则：
            1、后面超量阳线，"阳包阴"，
            2、两根内量能减半，

        2、序号不连续：
            中间阳线暂不处理，后面阴线必须缩量
        :return:
        """

        beginStatus = self.status
        headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
        # print(self._head)
        # print(headVolList)
        rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
        # print(self._rear)
        # print(rearVolList)

        if self._head[-1]['序号'] + 1 == self._rear[0]['序号']:
            """
            序号连续
            
            先判断是不是阶段性的最后一根
            
            条件：
            1、后面超量阳线，"阳包阴"，
            2、两根内量能缩量，
            3、本身就极度缩量，
            """
            # print('序号连续')
            """缩量情况系数"""
            k1 = 0.05
            try:
                # print(headVolList)
                # print(rearVolList)
                if sum(headVolList) and len(headVolList) and sum(rearVolList) and len(rearVolList):
                    self.status *= k1 * (
                        sum(headVolList) / len(headVolList) / (sum(rearVolList) / len(rearVolList)) - 1) + 1
                else:
                    self.status *= 1
            except IndexError or ZeroDivisionError:
                self.status *= 1
            """先判断是不是阶段性的最后一根"""
            try:
                if self.Index[self._rear[-1]['序号'] + 1]['布林'] < self._rear[0]['布林']:
                    self.status *= 1
                else:
                    try:
                        try:
                            if sum(headVolList) and len(headVolList) and sum(rearVolList) and len(rearVolList):
                                self.status *= k1 * (
                                    sum(headVolList) / len(headVolList) / (sum(rearVolList) / len(rearVolList)) - 1) + 1
                            else:
                                self.status *= 1
                        except IndexError or ZeroDivisionError:
                            self.status *= 1
                        try:
                            if max(rearVolList):
                                self.status *= k1 * (max(headVolList) / max(rearVolList) - 1) + 1
                            else:
                                self.status *= 1
                        except IndexError or ZeroDivisionError:
                            self.status *= 1
                    except IndexError:
                        self.status *= 1

                    """出现阳包阴时的放量系数"""
                    k2 = 0.02
                    """未出现阳包阴时的放量系数"""
                    k3 = 0.02
                    if self.Index[(self._rear[-1]['序号'] + 1)]['涨幅'] >= abs(self._rear[-1]['涨幅']):
                        "判定阳包阴"
                        try:
                            self.status *= k2 * (
                                self.Index[(self._rear[-1]['序号'] + 1)]['量能'] / self._rear[-1]['量能'] - 1) + 1
                        except IndexError or ZeroDivisionError:
                            self.status *= 1
                    elif self.Index[(self._rear[-1]['序号'] + 1)]['涨幅'] < abs(self._rear[-1]['涨幅']):
                        if self.Index[(self._rear[-1]['序号'] + 2)]['涨幅'] <= 0:
                            try:
                                if self.Index[(self._rear[-1]['序号'] + 1)]['量能']:
                                    self.status *= k3 * (
                                        self._rear[-1]['量能'] / self.Index[(self._rear[-1]['序号'] + 1)]['量能'] - 1) + 1
                                else:
                                    self.status *= 1
                            except IndexError or ZeroDivisionError:
                                self.status *= 1
                        else:
                            try:
                                if self.Index[(self._rear[-1]['序号'] + 1)]['量能'] + \
                                        self.Index[(self._rear[-1]['序号'] + 2)]['量能']:
                                    self.status *= k3 * (2 * self._rear[-1]['量能'] / (
                                        self.Index[(self._rear[-1]['序号'] + 1)]['量能'] +
                                        self.Index[(self._rear[-1]['序号'] + 2)]['量能']) - 1) + 1
                                else:
                                    self.status *= 1
                            except IndexError or ZeroDivisionError:
                                self.status *= 1
                    else:
                        self.status *= 1
            except IndexError or ZeroDivisionError:
                self.status *= 1

        elif self._head[-1]['序号'] + 1 < self._rear[0]['序号']:
            """
            序号不连续
            
            条件：
            1、平均值相对缩量；
            2、最后一根相对缩量；
            """
            # print('序号不连续')
            """缩量情况系数"""
            k = 0.125
            # headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
            # rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
            # # print((sum(headVolList)/len(headVolList) >= sum(rearVolList)/len(rearVolList)))
            # # print(k * max(headVolList) >= rearVolList[-1])
            try:
                p1 = (sum(headVolList) / len(headVolList)) / (sum(rearVolList) / len(rearVolList)) - 1
                p2 = max(headVolList) / rearVolList[-1] - 1
                self.status *= k * (p1 + p2) / 2 + 1
            except ZeroDivisionError:
                self.status *= 1
        else:
            self.status *= 1
        self._lastLevelResult = self.status / beginStatus

    def _index_hori_level(self):
        """
        水平层级差

        前后最大值必须相对缩量，
        同时，平均值缩量，
        或者，最小值缩量

        :return:
        """
        # headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
        # rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
        # if sum(headVolList) / len(headVolList) > sum(rearVolList) / len(rearVolList):
        #     self.status *= 1.5
        # elif min(headVolList) > min(rearVolList):
        #     self.status *= 1.5
        # else:
        #     self.status *= 0.75
        """水平层级差缩量占比系数"""
        """中间阳线"""
        k1 = 0.05
        """前后阴线"""
        k2 = 0.15

        beginStatus = self.status
        headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
        # print(self._head)
        # print(headVolList)
        rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
        # print(self._rear)
        # print(rearVolList
        midBullList = self._YY_VolumnList[(self._head[-1]['序号'] + 1):self._rear[0]['序号']]
        # if k * self._YY_VolumnList[self._rear[0]['序号']] > max(midBullList):
        #     self.status *= 0
        # else:
        #     self.status *= 1
        try:
            self.status *= k1 * (max(midBullList) / self._YY_VolumnList[self._rear[0]['序号']] - 1) + 1
        except ZeroDivisionError:
            self.status *= 1
        try:
            self.status *= k2 * ((sum(headVolList) / len(headVolList)) / (sum(rearVolList) / len(rearVolList)) - 1) + 1
        except ZeroDivisionError:
            self.status *= 1
        self._lastLevelResult = self.status / beginStatus

    def _cal_index(self, Kvalue):
        """
        计算K线的量化指标;
        划分阴阳序列;

        主要功能：
        在一次遍历中

        1、计算结合收针量能、日内交易均价等指标；
        2、重构新的K线信息列表，并不覆盖原始API数据

        3、分组划分阴阳线

        :param Kvalue:
        :return:
        """

        self._bull_length = 0
        self._bear_length = 0
        self._all_length = 0
        self.bull_por = -0.001
        self.patternResult = {}
        self.maxChange = 0
        self._raised = False
        self._fallTimes = 0
        self._lastFirstK = Kvalue[-1]
        self._lastSecondK = Kvalue[-2]

        """近期最高层级"""
        self._highestLevel = -10
        self._highestPrice = 0

        """层级和成功的层级差次数"""
        self.levelTimes = {'riseLevel': 0,
                           'riseResult': 0,
                           'horiLevel': 0,
                           'horiResult': 0,
                           'fallLevel': 0,
                           'fallResult': 0,
                           }

        self._seq_bull.clear()
        self._seq_bear.clear()
        self._list_bull.clear()
        self._list_bear.clear()
        self._seq.clear()
        self._levelList.clear()
        self.status = self._para['评分初值']

        if self.Index:
            self.Index.clear()
        self.Index = []
        s = None
        judge = None
        beared = False
        upSideMark = None
        # bottom = False
        t = []
        num = 0

        """
        1、计算  收针对量能的影响 
        2、分割阴阳线，重新构建序列
        """
        for Ksingle in Kvalue:
            """计算  收针对量能的影响 """
            temp = dict([(key, Ksingle[key]) for key in self._paraList])
            if temp['close'] > temp['open']:
                temp['量能'] = round(temp['volumn'] * (1 - self._para.get('收针对量能的影响系数', 1) * temp['上针'] / 100))
            else:
                temp['量能'] = round(temp['volumn'] * (1 - self._para.get('收针对量能的影响系数', 1) * temp['下针'] / 100))

            """
            布林为基准的底部判断。
            中下轨的下部空间
            '布林' <= -2
            """
            if temp['布林'] <= -2:
                temp['底部'] = True
            else:
                temp['底部'] = False

            """
            judge：当前K线是阴线还是阳线的标志
            beared：是否已经出现过阴线的标志
            
            划分阴阳序列
            s：当前序列是阴线还是阳线的标志
            s = {0: None, 'bull': 1, 'bear': 2}
            
            self._list_bull.clear()
            self._list_bear.clear()
            """

            if temp['close'] > temp['lastclose']:
                judge = True
                temp['趋势'] = True
            elif temp['close'] == temp['lastclose']:
                if temp['close'] >= temp['open']:
                    judge = True
                    temp['趋势'] = True
                elif temp['close'] < temp['open']:
                    judge = False
                    temp['趋势'] = False
                else:
                    judge = None
                    raise ValueError('我也不知道为啥judge的值不对!或许是打开方式不对!', judge)
            elif temp['close'] < temp['lastclose']:
                judge = False
                temp['趋势'] = False
            else:
                judge = None
                raise ValueError('我也不知道为啥judge的值不对!或许是打开方式不对!', judge)

            """
            序列以阴线序列开始
            """
            if beared or judge is False:
                beared = True
            else:
                continue
            temp['序号'] = num
            num += 1
            self.maxChange = max(self.maxChange, temp['涨幅'])
            self.Index.append(temp)
            if not s:
                """not s：未判断"""
                self.minVol = temp['volumn']
                if judge:
                    s = 1
                else:
                    s = 2
            self.minVol = min(temp['volumn'], self.minVol)
            if s == 1:
                if judge:
                    self._list_bull.append(temp)
                else:
                    s = 2
                    t = self._list_bull[:]
                    self._seq.append(t)
                    self._seq_bull.append(t)
                    self._list_bear.clear()
                    self._list_bear.append(temp)
            elif s == 2:
                if not judge:
                    self._list_bear.append(temp)
                else:
                    s = 1
                    t = self._list_bear[:]
                    self._seq.append(t)
                    self._seq_bear.append(t)
                    self._list_bull.clear()
                    self._list_bull.append(temp)
            else:
                raise ValueError('我也不知道为啥s的值不对!或许是打开方式不对!', s)
        if s == 1:
            if judge:
                t = self._list_bull[:]
                self._seq_bull.append(t)
        elif s == 2:
            if not judge:
                t = self._list_bear[:]
                self._seq_bear.append(t)
        else:
            raise ValueError('我也不知道为啥s的值不对!或许是打开方式不对!', s)
        self._seq.append(t)

        """
        下面开始分段拆分层级
        再用一次遍历，同时：
        1、找到最后一个底部区间，布林层面上的下部区间（下轨下层）；
            注意、连续的bottom则以价格为准
            找到最低的阶段性底部
        2、将阴线序列按照层级拆分开；
        """

        """
        层级
        """
        # last_level = None
        low_level = 100

        """
        最低
        """
        # last_price = None
        min_price = 100000.00

        level_temp = []
        # last_level = None
        breakMark = None
        for array in self._seq_bear[::-1]:
            # element = {'布林': 0}
            last_level = None
            for element in array[::-1]:
                if low_level <= -2 < element['布林'] and min_price <= element['close']:
                    breakMark = True
                    break
                if element['布林'] == last_level:
                    level_temp.append(element)
                else:
                    last_level = element['布林']
                    if level_temp:
                        self._levelList.append(level_temp[:])
                    # level_temp.clear()
                    #     level_temp.append(element)
                    # else:
                    level_temp.clear()
                    level_temp.append(element)
                low_level = min(low_level, element['布林'])
                min_price = min(min_price, element['close'])
            if breakMark:
                break
        # endArray = level_temp[:]
        # if len(endArray) > 1:
        #     endArray.pop()
        #     self._levelList.append(endArray)
        # else:
        #     pass
        # for i in self._levelList:
        #     print(i)
        try:
            if self._levelList[-1][-1]['布林'] >= self._levelList[-2][-1]['布林']:
                temp = self._levelList.pop()
                self._bull_length -= len(temp)
        except IndexError:
            pass

        # print(self._seq)
        # print(self._seq_bear)
        # print(self._levelList)
        self._bear_length = sum(len(l) for l in self._levelList)
        if self._levelList:
            _levelList = self._levelList[-1][-1]['序号']
        else:
            _levelList = 0
        self._all_length = self._seq[-1][-1]['序号'] - _levelList + 1
        self._bull_length = self._all_length - self._bear_length
        # print(self._all_length)
        # print(self._bull_length)
        # print(self._bear_length)
        """
        功能：
        1、找到符合层级形态的
            +1：中上轨下部空间
            0：等于中轨
            -1：中下轨上部空间
        2、上升层级中间阳线必须放量，绝对放量！！！
        3、下降层级后的3根K线内（含阴线组内阴线）必须出地量同层，或者放量上层！
        """
        self._YY_VolumnList = [l['量能'] for l in self.Index]
        self._levelList.reverse()
        for i in self._levelList:
            if len(i) > 1:
                i.reverse()
        for i in range(len(self._levelList) - 1):
            if self.status == 0:
                break
            self._head = self._levelList[i][:]
            self._rear = self._levelList[i + 1][:]
            # print(self._head[0]['time'])
            # print(self._rear[0]['time'])

            """判断是否位上部区间，同时计算近期最高层级，若层级新高 self._fallTimes 重置"""
            # upSideMark = None
            if upSideMark:
                thisMaxPrice = max([k['close'] for k in self.Index[self._head[0]['序号']:self._rear[0]['序号']]])
                # print(self.Index[self._head[0]['序号']:self._rear[0]['序号']])
                # print(thisMaxPrice)
                if self._head[0]['布林'] > self._highestLevel \
                        or (self._head[0]['布林'] >= 1 and thisMaxPrice >= self._highestPrice):
                    self._highestLevel = max(self._head[0]['布林'], self._highestLevel)
                    self._highestPrice = max(self._highestPrice, thisMaxPrice)
                    self._fallTimes = 0
                    self._raised = True
            elif self._head[0]['布林'] >= 1:
                upSideMark = True
            else:
                upSideMark = False

            """
            先不判断连续阴线
            """
            "self._setPrint 是否打印"
            breakMark = None
            if len(self._levelList[i]) > 1:
                self._index_cont_bear()
                # print(self._head)
                if self._setPrint:
                    print('连续阴线，结果：' + format(self.status, '0.3f'))

            """计算 层级和成功的层级差次数"""
            if self.status >= 0:
                self._lastLevelName = ''
                self._lastLevelResult = 1
                if self._head[0]['布林'] > self._rear[0]['布林']:
                    if upSideMark:
                        if self._raised:
                            self._fallTimes += 1
                            self._raised = False
                    self._index_fall_level()
                    self._lastLevelName = '下降层级'
                    self.levelTimes['riseLevel'] += 1
                    if self._lastLevelResult >= 1:
                        self.levelTimes['riseResult'] += 1
                    if self._setPrint:
                        print('下降层级，结果：' + format(self.status, '0.3f'))
                elif self._head[0]['布林'] == self._rear[0]['布林']:
                    self._index_hori_level()
                    self._lastLevelName = '水平层级'
                    self.levelTimes['horiLevel'] += 1
                    if self._lastLevelResult >= 1:
                        self.levelTimes['horiResult'] += 1
                    if self._setPrint:
                        print('水平层级，结果：' + format(self.status, '0.3f'))
                elif self._head[0]['布林'] < self._rear[0]['布林']:
                    self._index_rise_level()
                    self._lastLevelName = '上升层级'
                    self.levelTimes['fallLevel'] += 1
                    if upSideMark:
                        self._raised = True
                    if self._lastLevelResult >= 1:
                        self.levelTimes['fallResult'] += 1
                    if self._setPrint:
                        print('上升层级，结果：' + format(self.status, '0.3f'))
                else:
                    breakMark = True
            if breakMark:
                break

        """ 阳线占比 """
        self.bull_por = 100 * (self._bull_length / self._all_length)
        if self._setPrint:
            print('阳线占比：' + format(self.bull_por, '0.3f'))
            print('最终结果：' + format(self.status, '0.3f'))

        # 1、注意底部起来的连续阳线；

        """
        未完成的任务：
        2、计算水平，上升和下降层级差，不同的层级差对中间阳线的量能要求不一样
            （也是就放量和地量的出现需求）
            
            例如，高层地量和次地量，中下层的山峰技术形态
        
        6、U型反弓：
            1、三条轨道都要进入一个反弓状态；
            2、在反弓的底部量能不能有急剧的变化；
            3、U形反弓的右侧要放量，这个右侧界定的标准：至少是翘头的；）
            布林中轨最小值 和 下轨接近的位置 是 关键节点！
            层级差是技术形态，结合趋势和量价关系！
            
        """

    def cal_patternResult(self, KtimeType='day'):
        """
        计算各种形态结果
        :return:
        """
        self._pattern_001_144BollUpper20BollUpside()
        # self._pattern_100_20BollAnd144BollFirstWave()
        if KtimeType == 'day':
            # self._pattern_002_20DayBollRaiseAndHoriLevel()
            self._pattern_003_Day9Bears()
        self._pattern_101_20BollDayAnd60fDoubleB3(KtimeType)

    def _pattern_001_144BollUpper20BollUpside(self):
        """
        形态001：
        144上轨穿 20布林的上部区间 K线近中轨

        过滤标准：
        1、144上柜在20布林上部空间，靠上不靠下，中间位置最好
        2、打出技术形态优先
        3、20日三轨上扬初期，第一第二个回调为佳
            我现在的方法是，摸一次中上轨上部区间，再回到中上轨下部区间及以下，算回调。
        4、k线尽量回在中轨附近
        5、k线最好在144上轨下
        6、最近有较好涨幅优先
            20日三轨上扬初期，开始计算，10天

        :return:
        """
        # print(self.Index[-1])
        patternResult = {'序号': '001',
                         '名称': '144上轨穿 20布林的上部区间 K线近中轨',
                         '结果': 0,
                         '近期层级类型': None,
                         '层级差得分': 0,
                         '回调次数': 0,
                         'K线位于20布林位置': None,
                         'K线位于144布林位置': None,
                         '近期最大涨幅': 0,
                         }
        upper_mid = (self.Index[-1]['mid'] + self.Index[-1]['upper']) / 2
        if (self.Index[-1]['mid'] <= self.Index[-1]['upper144'] <= self.Index[-1]['upper']) and \
                (self.Index[-1]['mid'] < min(self.Index[-1]['open'], self.Index[-1]['close']) <= upper_mid):
            patternResult['结果'] = 1
        else:
            self.patternResult['001_144BollUpper20BollUpside'] = patternResult
            return
        # print(self.Index[-1])
        patternResult['近期层级类型'] = self._lastLevelName
        patternResult['层级差得分'] = round(self._lastLevelResult * 100, 3)
        patternResult['回调次数'] = self._fallTimes
        patternResult['K线位于20布林位置'] = self.Index[-1]['布林']
        patternResult['K线位于144布林位置'] = self.Index[-1]['144布林']
        patternResult['近期最大涨幅'] = self.maxChange
        # print(patternResult)
        self.patternResult['001_144BollUpper20BollUpside'] = patternResult

    def _pattern_002_20DayBollRaiseAndHoriLevel(self):
        """
        形态002：
        20日布林的上升和水平层级差

        过滤标准：
        1、日线级别20布林的上升和水平层级差

        :return:
        """
        # print(self.Index[-1])
        patternResult = {'序号': '002',
                         '名称': '日线级别20布林的上升和水平层级差',
                         '结果': 0,
                         '近期层级类型': None,
                         '层级差得分': 0,
                         '回调次数': 0,
                         'K线位于20布林位置': None,
                         'K线位于144布林位置': None,
                         '近期最大涨幅': 0,
                         }
        self.patternResult['002_20DayBollRaiseAndHoriLevel'] = patternResult
        length002 = 15
        valueList002 = self.Index[-length002:][::-1]
        # 'open' 'close' 'lastclose'
        # 判断层级差
        status002 = 0
        # status002 = 1
        firstBearList = []
        # status002 = 2
        firstBullList = []
        # status002 = 3
        secondBearList = []
        # status002 = 4
        secondBullList = []
        if valueList002[0]['close'] <= valueList002[0]['lastclose']\
                and valueList002[0]['close'] <= valueList002[0]['open']:
            for element002 in valueList002:
                if element002['close'] <= element002['lastclose'] \
                        and element002['close'] <= element002['open']:
                    if status002 == 0 or status002 == 2:
                        status002 += 1
                    if status002 == 1:
                        firstBearList.append(element002)
                    elif status002 == 3:
                        secondBearList.append(element002)
                else:
                    if status002 == 0:
                        pass
                    elif status002 == 1 or status002 == 3:
                        status002 += 1
                    if status002 == 2:
                        firstBullList.append(element002)
                    elif status002 == 4:
                        secondBullList.append(element002)
            if 3 >= len(secondBearList) >= 2 and 3 >= len(firstBearList) >= 1:
                if (secondBearList[0]['布林'] <= firstBearList[-1]['布林'])\
                        and (max([k['量能'] for k in secondBearList]) >= min([k['量能'] for k in firstBearList])):
                    patternResult['结果'] = 1
        # print(self.Index[-1])
        patternResult['近期层级类型'] = self._lastLevelName
        patternResult['层级差得分'] = round(self._lastLevelResult * 100, 3)
        patternResult['回调次数'] = self._fallTimes
        patternResult['K线位于20布林位置'] = self.Index[-1]['布林']
        patternResult['K线位于144布林位置'] = self.Index[-1]['144布林']
        patternResult['近期最大涨幅'] = self.maxChange
        # print(patternResult)
        self.patternResult['002_20DayBollRaiseAndHoriLevel'] = patternResult

    def _pattern_003_Day9Bears(self):
        """
        形态002：
        20日布林的上升和水平层级差

        过滤标准：
        1、日线级别20布林的上升和水平层级差

        :return:
        """
        # print(self.Index[-1])
        patternResult = {'序号': '002',
                         '名称': '日线级别20布林的上升和水平层级差',
                         '结果': 0,
                         '近期层级类型': None,
                         '层级差得分': 0,
                         '回调次数': 0,
                         'K线位于20布林位置': None,
                         'K线位于144布林位置': None,
                         '近期最大涨幅': 0,
                         }
        self.patternResult['002_20DayBollRaiseAndHoriLevel'] = patternResult
        length002 = 15
        valueList002 = self.Index[-length002:][::-1]
        # 'open' 'close' 'lastclose'
        # 判断层级差
        status002 = 0
        # status002 = 1
        firstBearList = []
        # status002 = 2
        firstBullList = []
        # status002 = 3
        secondBearList = []
        # status002 = 4
        secondBullList = []
        if valueList002[0]['close'] <= valueList002[0]['lastclose'] \
                and valueList002[0]['close'] <= valueList002[0]['open']:
            for element002 in valueList002:
                if element002['close'] <= element002['lastclose'] \
                        and element002['close'] <= element002['open']:
                    if status002 == 0 or status002 == 2:
                        status002 += 1
                    if status002 == 1:
                        firstBearList.append(element002)
                    elif status002 == 3:
                        secondBearList.append(element002)
                else:
                    if status002 == 0:
                        pass
                    elif status002 == 1 or status002 == 3:
                        status002 += 1
                    if status002 == 2:
                        firstBullList.append(element002)
                    elif status002 == 4:
                        secondBullList.append(element002)
            if 3 >= len(secondBearList) >= 2 and 3 >= len(firstBearList) >= 1:
                if (secondBearList[0]['布林'] <= firstBearList[-1]['布林']) \
                        and (max([k['量能'] for k in secondBearList]) >= min([k['量能'] for k in firstBearList])):
                    patternResult['结果'] = 1
        # print(self.Index[-1])
        patternResult['近期层级类型'] = self._lastLevelName
        patternResult['层级差得分'] = round(self._lastLevelResult * 100, 3)
        patternResult['回调次数'] = self._fallTimes
        patternResult['K线位于20布林位置'] = self.Index[-1]['布林']
        patternResult['K线位于144布林位置'] = self.Index[-1]['144布林']
        patternResult['近期最大涨幅'] = self.maxChange
        # print(patternResult)
        self.patternResult['002_20DayBollRaiseAndHoriLevel'] = patternResult

    def _pattern_100_20BollAnd144BollFirstWave(self):
        """
        形态100：
        4B打法的底部20布林和144布林的一次启动

        过滤标准：
        1、20 B3（上半空间下部） 、144 >=3 首次 开始统计下降层级差 V U次数 <=2

        日线，20、144
        60F，20、144
        一次启动关系，先确认

        :return:
        """
        # print(self.Index[-1])
        patternResult = {'序号': '100',
                         '名称': '4B打法的底部20布林和144布林的一次启动',
                         '结果': 0,
                         '近期层级类型': None,
                         '层级差得分': 0,
                         '回调次数': 0,
                         'K线位于20布林位置': None,
                         'K线位于144布林位置': None,
                         '近期最大涨幅': 0,
                         }
        upper_mid = (self.Index[-1]['mid'] + self.Index[-1]['upper']) / 2
        if (self.Index[-1]['mid'] <= self.Index[-1]['upper144'] <= self.Index[-1]['upper']) and \
                (self.Index[-1]['mid'] < min(self.Index[-1]['open'], self.Index[-1]['close']) <= upper_mid):
            patternResult['结果'] = 1
        else:
            self.patternResult['100_20BollAnd144BollFirstWave'] = patternResult
            return
        # print(self.Index[-1])
        patternResult['近期层级类型'] = self._lastLevelName
        patternResult['层级差得分'] = round(self._lastLevelResult * 100, 3)
        patternResult['回调次数'] = self._fallTimes
        patternResult['K线位于20布林位置'] = self.Index[-1]['布林']
        patternResult['K线位于144布林位置'] = self.Index[-1]['144布林']
        patternResult['近期最大涨幅'] = self.maxChange
        # print(patternResult)
        self.patternResult['100_20BollAnd144BollFirstWave'] = patternResult

    def _pattern_101_20BollDayAnd60fDoubleB3(self, KtimeType):
        # print(self._lastFirstK)
        # print(self._lastSecondK)
        if KtimeType == 'day':
            # print(KtimeType)
            self._pattern_101_20BollDay4B()
        elif KtimeType == '60':
            # print(KtimeType)
            self._pattern_101_20Boll60F4B()
        else:
            raise ValueError("KtimeType输入值不正确! 输入值为：", str(KtimeType))

    def _pattern_101_20BollDay4B(self):
        """
        形态101：
        20布林day和60F双B3

        过滤标准：
        1、20布林day和60F双上半空间下部
            关键触发条件

        2、首次 布林位置>= -1 之后，下降次数<=2，到达更高层级时重置次数
            day和60F布林位置 均>= -1 至少一个 >=1
            下降层级次数<=5次
            近期层级类型 60F上
            近期层级差必须有效

        3、统计阳线占比、各类层级差次数

        日线，20
        60F，20
        一次启动关系，先确认

        具体实现：
            1、布林位置>= -1
            2、回调次数<= 2（上升后再计算，一共计算到两次）备选下降层级次数<=5次
            3、阳线优势
            4、列出 层级和层级差次数
            5、日线添加强上攻形态，上轨支撑
        :return:
        """
        # print(self.Index[-1])
        patternResult = {'序号': '101',
                         '名称': '20布林day的4B打法',
                         '结果': 0,
                         '近期层级类型': None,
                         '层级差得分': 0,
                         '回调次数': 0,
                         'K线位于20布林位置': None,
                         '中轨状态': 0,
                         'K线位于144布林位置': None,
                         '近期最大涨幅': 0,
                         '阳线占比': 0,
                         'K线概况':
                             {
                                 '阳线数': 0,
                                 '阴线数': 0,
                                 '总数': 0,
                             },
                         '层级和层级差次数':
                             {
                                 'riseLevel': 0,
                                 'riseResult': 0,
                                 'horiLevel': 0,
                                 'horiResult': 0,
                                 'fallLevel': 0,
                                 'fallResult': 0,
                             }
                         }
        """结合轨距判断"""
        if self.Index[-1]['布林'] >= 2:
            if self._fallTimes == 0:
                patternResult['结果'] = 1
            elif self._fallTimes == 1 and self.Index[-1]['轨距'] >= 6:
                patternResult['结果'] = 1
            elif 1 >= self.Index[-1]['布林'] >= -1 and self._lastLevelName != '下降层级':
                if self._fallTimes == 0:
                    patternResult['结果'] = 1
                elif self._fallTimes == 1 and self.Index[-1]['轨距'] >= 6:
                    patternResult['结果'] = 1
        else:
            self.patternResult['101_20BollDay4B'] = patternResult
            return
        # print(self.Index[-1])
        if self._lastFirstK['mid'] > self._lastSecondK['mid']:
            patternResult['中轨状态'] = 1
        if self._lastFirstK['mid'] < self._lastSecondK['mid']:
            patternResult['中轨状态'] = -1
        patternResult['近期层级类型'] = self._lastLevelName
        patternResult['层级差得分'] = round(self._lastLevelResult * 100, 3)
        patternResult['回调次数'] = self._fallTimes
        patternResult['K线位于20布林位置'] = self.Index[-1]['布林']
        patternResult['K线位于144布林位置'] = self.Index[-1]['144布林']
        patternResult['近期最大涨幅'] = self.maxChange
        patternResult['阳线占比'] = round(self.bull_por, 3)
        patternResult['K线概况']['阳线数'] = self.get_bull_length()
        patternResult['K线概况']['阴线数'] = self.get_bear_length()
        patternResult['K线概况']['总数'] = self.get_all_length()
        patternResult['层级和层级差次数'] = self.levelTimes
        # print(patternResult)
        self.patternResult['101_20BollDay4B'] = patternResult

    def _pattern_101_20Boll60F4B(self):
        """
        形态101：
        20布林day和60F双B3

        过滤标准：
        1、20布林day和60F双上半空间下部
            关键触发条件

        2、首次 布林位置>= -1 之后，下降次数<=2，到达更高层级时重置次数
            day和60F布林位置 均>= -1 至少一个 >=1
            下降层级次数<=5次
            近期层级类型 60F上
            近期层级差必须有效

        3、统计阳线占比、各类层级差次数

        日线，20
        60F，20
        一次启动关系，先确认

        具体实现：
            1、布林位置>= -2
            2、回调次数<= 1（上升后再计算，一共计算到两次）备选下降层级次数<=5次
            3、阳线优势
            4、列出 层级和层级差次数
            5、近期不是下降层级
        :return:
        """
        # print(self.Index[-1])
        patternResult = {'序号': '101',
                         '名称': '20布林60F的4B打法',
                         '结果': 0,
                         '近期层级类型': None,
                         '层级差得分': 0,
                         '回调次数': 0,
                         'K线位于20布林位置': None,
                         '中轨状态': 0,
                         'K线位于144布林位置': None,
                         '近期最大涨幅': 0,
                         '阳线占比': 0,
                         'K线概况':
                             {
                                 '阳线数': 0,
                                 '阴线数': 0,
                                 '总数': 0,
                             },
                         '层级和层级差次数':
                             {
                                 'riseLevel': 0,
                                 'riseResult': 0,
                                 'horiLevel': 0,
                                 'horiResult': 0,
                                 'fallLevel': 0,
                                 'fallResult': 0,
                             }
                         }
        """结合轨距判断"""
        if self.Index[-1]['布林'] >= 2:
            if self._fallTimes == 0:
                patternResult['结果'] = 1
            elif self._fallTimes == 1 and self.Index[-1]['轨距'] >= 2:
                patternResult['结果'] = 1
        elif 1 >= self.Index[-1]['布林'] >= -1 and self._lastLevelName != '下降层级':
            if self._fallTimes == 0:
                patternResult['结果'] = 1
            elif self._fallTimes == 1 and self.Index[-1]['轨距'] >= 2:
                patternResult['结果'] = 1
        else:
            self.patternResult['101_20Boll60F4B'] = patternResult
            return
        # print(self.Index[-1])
        if self._lastFirstK['mid'] > self._lastSecondK['mid']:
            patternResult['中轨状态'] = 1
        if self._lastFirstK['mid'] < self._lastSecondK['mid']:
            patternResult['中轨状态'] = -1
        patternResult['近期层级类型'] = self._lastLevelName
        patternResult['层级差得分'] = round(self._lastLevelResult * 100, 3)
        patternResult['回调次数'] = self._fallTimes
        patternResult['K线位于20布林位置'] = self.Index[-1]['布林']
        patternResult['K线位于144布林位置'] = self.Index[-1]['144布林']
        patternResult['近期最大涨幅'] = self.maxChange
        patternResult['阳线占比'] = round(self.bull_por, 3)
        patternResult['K线概况']['阳线数'] = self.get_bull_length()
        patternResult['K线概况']['阴线数'] = self.get_bear_length()
        patternResult['K线概况']['总数'] = self.get_all_length()
        patternResult['层级和层级差次数'] = self.levelTimes
        # print(patternResult)
        self.patternResult['101_20Boll60F4B'] = patternResult

"""
中轨必须至少一个是上行的。

144BollUpper20BollUpside
7、k线直接到达下轨，坐轨就打
"""
