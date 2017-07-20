import math

from functions import getValue


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
                        'KgetLength': 10,
                        'TdayLength': 5,
                        'TgetLength': 1,
                        'appcode': 'c7689f18e1484e9faec07122cc0b5f9e'}
        self.code = code
        self._ref_list = ref_List
        self.Kvalue = None
        self.Tvalue = None
        # self.value = self.get_KValue()
        self.Kstatus = {'涨幅': 0, '开收': 0, '量能': 0, '上针': 0, '下针': 0,
                        '布林': 0, '轨距': 0, '层级': '', '趋势': None, '底部': None,
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
                self.Kvalue = getValue.get_60F(self.code, self._ref_list['KbeginDay'],
                                               self._ref_list['KgetLength'])
            elif self._ref_list['KtimeType'] == 'day':
                self.Kvalue = getValue.get_dayK(self.code, self._ref_list['KbeginDay'],
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
        bollmid = self.Kvalue[-1-n]['mid']
        return bollmid


    def boll_upper(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self._get_KLine()
        bollupper = self.Kvalue[-1-n]['upper']
        return bollupper


    def boll_lower(self, n=0):
        """
        直接获得K线Boll数据
        :return:
        """
        if self.Kvalue is None:
            self._get_KLine()
        bolllower = self.Kvalue[-1-n]['lower']
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
                self.update_K参数(_Kvalue)
                _Kvalue.update(self.Kstatus)
                self.Kvalue[i] = _Kvalue
                i += 1


    # def clear_Kstatus(self):
    #     self.Kstatus = None


    def update_K参数(self, _Kvalue):
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
        except ZeroDivisionError:
            self.Kstatus['涨幅'] = 0
            self.Kstatus['开收'] = 0
            self.Kstatus['上针'] = 0.00
            self.Kstatus['下针'] = 0.00
            self.Kstatus['轨距'] = 0.00
            self.Kstatus['布林'] = 0
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
            except ZeroDivisionError:
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
        self._list_bull = []
        self._list_bear = []
        self._seq_bull = []
        self._seq_bear = []
        self._seq = []
        self._levelList = []
        self._head = []
        self._rear = []
        self._paraList = ['序号', 'time', 'open', 'min', 'max', 'close', 'lastclose', 'volumn',
                          'upper', 'mid',  'lower', '涨幅', '开收', '量能', '上针',
                          '下针', '布林', '底部', '轨距', '层级', '趋势', '平台']

        """minVol 近期地量"""
        self.minVol = 0
        self._YY_VolumnList = None
        if para is None:
            para = {'收针对量能的影响系数': 0.75,
                    '评分初值': 100
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
        # k = 1.5
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
        k = 0.1
        self.status *= k * ((sum(preBearList) / len(preBearList)) / lastBear['量能'] - 1) + 1


    def _index_rise_level(self):
        """
        上升层级差，中间必有阳线，阳线放量（两侧阴线最大值的k倍率）

        注意：
        初版暂时没考虑涨停的情况，观察一下效果，后续修改

        :return:
        """
        """上升层级差缩量占比系数"""
        """中间阳线"""
        k1 = 0.16
        """前后阴线"""
        k2 = 0.12
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
        except ValueError:
            self.status *= 1
        try:
            if len(headVolList) != 0 and len(rearVolList) != 0 and sum(rearVolList) != 0:
                self.status *= k2 * ((sum(headVolList) / len(headVolList)) / (sum(rearVolList) / len(rearVolList)) - 1) + 1
            else:
                self.status *= 1
        except ValueError:
            self.status *= 1

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
            k = 2
            headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
            # print(self._head)
            # print(headVolList)
            rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
            # print(self._rear)
            # print(rearVolList)
            if self.Index[self._rear[-1]['序号'] + 1]['布林'] < self._rear[0]['布林']:
                self.status *= 1
            elif sum(headVolList) / len(headVolList) > k * sum(rearVolList) / len(rearVolList):
                self.status *= 1
            elif max(headVolList) > k * max(rearVolList):
                self.status *= 1
            else:
                "阳包阴"
                if (self.Index[(self._rear[-1]['序号'] + 1)]['涨幅'] > abs(self._rear[-1]['涨幅'])) and (self.Index[(self._rear[-1]['序号'] + 1)]['量能'] > self._rear[-1]['量能']):
                    self.status *= 1
                elif k * self.Index[(self._rear[-1]['序号'] + 1)]['量能'] < self._rear[-1]['量能']:
                    self.status *= 1
                elif (k * self.Index[(self._rear[-1]['序号'] + 2)]['量能'] < self._rear[-1]['量能']) and (self.Index[(self._rear[-1]['序号'] + 1)]['涨幅'] > 0):
                    self.status *= 1
                else:
                    self.status *= 0
        elif self._head[-1]['序号'] + 1 < self._rear[0]['序号']:
            """
            序号不连续
            
            条件：
            1、平均值相对缩量；
            2、最后一根相对缩量；
            """
            # print('序号不连续')
            k = 1.25
            headVolList = self._YY_VolumnList[self._head[0]['序号']:(self._head[-1]['序号'] + 1)]
            rearVolList = self._YY_VolumnList[self._rear[0]['序号']:(self._rear[-1]['序号'] + 1)]
            # print((sum(headVolList)/len(headVolList) >= sum(rearVolList)/len(rearVolList)))
            # print(k * max(headVolList) >= rearVolList[-1])
            if (sum(headVolList)/len(headVolList) >= sum(rearVolList)/len(rearVolList) and
                    k * max(headVolList) >= rearVolList[-1]):
                self.status *= 1
            else:
                self.status *= 0
        else:
            self.status *= 1


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
        k2 = 0.1
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
        self.status *= k1 * (max(midBullList) / self._YY_VolumnList[self._rear[0]['序号']] - 1) + 1
        self.status *= k2 * ((sum(headVolList) / len(headVolList)) / (sum(rearVolList) / len(rearVolList)) - 1) + 1

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
                temp['量能'] = round(temp['volumn']*(1-self._para.get('收针对量能的影响系数', 1)*temp['上针']/100))
            else:
                temp['量能'] = round(temp['volumn']*(1-self._para.get('收针对量能的影响系数', 1)*temp['下针']/100))

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
                    #     level_temp.clear()
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
                self._levelList.pop()
        except IndexError:
            pass

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

            """
            先不判断连续阴线
            """
            if len(self._levelList[i]) > 1:
                self._index_cont_bear()
                # print(self._head)
                # print('连续阴线，结果：' + str(self.status))
            if self.status >= 0:
                if self._head[0]['布林'] > self._rear[0]['布林']:
                    self._index_fall_level()
                    # print('下降层级，结果：' + str(self.status))
                elif self._head[0]['布林'] == self._rear[0]['布林']:
                    self._index_hori_level()
                    # print('水平层级，结果：' + str(self.status))
                elif self._head[0]['布林'] < self._rear[0]['布林']:
                    self._index_rise_level()
                    # print('上升层级，结果：' + str(self.status))
                else:
                    break
        # print('最终结果：' + str(self.status))
        for 注意底部起来的连续阳线。


        """
        +4：高于上轨
        +3：等于上轨
        +2：中上轨上部空间
        +1：中上轨下部空间
        0：等于中轨
        -1：中下轨上部空间
        -2：中下轨下部空间
        -3：等于下轨
        -4：低于下轨
        """


        """
        未完成的任务：
        1、找到布林下轨起点:
            也就是最小的布林分层位置（这个位置就是短期底部）;
        2、按照K线布林分层，把阴线分段：
            计算水平，上升和下降层级差，不同的层级差对中间阳线的量能要求不一样
            （也是就放量和地量的出现需求）
            例如，高层地量和次地量，中下层的山峰技术形态
        3、逐层分段计算并审核层级差;
        4、连续和不连续阴线的分组处理
        
        5、beta 0.1 暂时不考虑阳线
        
        6、U型反弓：
            1、三条轨道都要进入一个反弓状态；
            2、在反弓的底部量能不能有急剧的变化；
            3、U形反弓的右侧要放量，这个右侧界定的标准：至少是翘头的；）
            布林中轨最小值 和 下轨接近的位置 是 关键节点！
            层级差是技术形态，结合趋势和量价关系！
            
        """

