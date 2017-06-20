from functions import getValue


class Stock:
    """
    stock类的测试版
    code: 代码
    ref_list: 包含timetype、beginDay、appcode等在内其他参数字典
    """
    def __init__(self, code, ref_List):
        if ref_List is None:
            ref_List = {'timetype': '60/day',
                        'beginDay': '20170101',
                        'getLength': 10,
                        'appcode': 'c7689f18e1484e9faec07122cc0b5f9e'}
        self.code = code
        self.ref_list = ref_List
        self.value = None


    def get_KLine(self):
        """
        计算各级别的K线
        :return:
        """
        try:
            if self.ref_list['timetype'] == '60':
                self.value = getValue.get_60F(self.code, self.ref_list['beginDay'], self.ref_list['getLength'])
            elif self.ref_list['timetype'] == 'day':
                self.value = getValue.get_dayK_Line(self.code, self.ref_list['beginDay'], self.ref_list['getLength'])
        except ValueError:
            pass


    def get_KValue(self):
        if self.value is None:
            self.get_KLine()
            return self.value
        else:
            return self.value
