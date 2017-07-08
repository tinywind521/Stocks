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
                        '平台': '', '预留': '', '备用': ''}


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
        self._paraList = ['time', 'open', 'min', 'max', 'close', 'lastclose', 'volumn',
                          'upper', 'mid',  'lower', '涨幅', '开收', '量能', '上针',
                          '下针', '布林', '底部', '轨距', '层级', '趋势', '平台']
        self.minVol = 0
        self._YYstatus = None
        if para is None:
            para = {'收针对量能的影响系数': 0.75,

                    }
            self._para = para
        if Kvalue is None or len(Kvalue) == 0:
            # Kvalue = Stock.get_KValue()
            raise ValueError('input Kvalue is None!')
        else:
            self._para = para
            self.Index = None

            """Index 为量化指标"""
            self._cal_index(Kvalue)

            """minVol 近期地量"""

        # [{[{}], {}}]
        # { [ {连续K线1参数 }, {连续K线2参数}, {连续K线3参数}...], {第2组连续K线的组参数} },


    def get_para(self):
        return self._para


    def get_seq_bull(self):
        return self._seq_bull


    def get_seq_bear(self):
        return self._seq_bear


    def get_seq_all(self):
        return self._seq


    def refresh_index(self, Kvalue):
        """
        刷新K线量化指标
        :param Kvalue:
        :return:
        """
        self._cal_index(Kvalue)


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

        if self.Index:
            self.Index.clear()
        self.Index = []
        s = None
        judge = None
        beared = False
        bottom = False
        # above_mid = False
        for Ksingle in Kvalue:
            """计算  收针对量能的影响 """
            temp = dict([(key, Ksingle[key]) for key in self._paraList])
            if temp['close'] > temp['open']:
                temp['量能'] = round(temp['volumn']*(1-self._para.get('收针对量能的影响系数', 1)*temp['上针']/100))
            else:
                temp['量能'] = round(temp['volumn']*(1-self._para.get('收针对量能的影响系数', 1)*temp['下针']/100))

            self.Index.append(temp)
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
                if temp['close'] > temp['open']:
                    judge = True
                    temp['趋势'] = True
                elif temp['close'] <= temp['open']:
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

            if beared or judge is False:
                beared = True
            else:
                continue

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
        已完成：
        1、序列以阴线序列开始；
        2、关于短期/中期底部的判定：
            首先、布林层面上的下部区间（下轨下层）
            其次、遇到过程中到了中轨以上，就刷新标志位
            最后、分析时找到最后一个下部区间
            注意、连续的bottom则以价格为准
        3、
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
        
        """

