from functions import getValue
from functions import function
from aliyun import aliyun_api
import json
import numpy


codeList = getValue.get_availableCodeList()
# 获取有效代码列表
dateList = getValue.get_dateList('20170101', 10)
# 获取K线的起始日期

level_differList = []
# 初始化层级差列表
n = 20
# 判断K线长度的常量
for code in codeList:
    s = getValue.get_60F(code, dateList[0], 10, n)
    # print(s)
    # 获取60F K线列表，共10天的数据内的n条K线
    k_list = []
    first_N = []
    first_close = []
    first_vol = []
    second_N = []
    second_close = []
    second_vol = []
    passiveList = []
    if len(s) == n:
        for element in s[::-1]:
            element['open'] = float(element['open'])
            element['close'] = float(element['close'])
            element['volumn'] = int(element['volumn'])
            # 把字符串转化为浮点数字
            k_list.append(element)
            # 重新构建K线列表，元素是字典element
        # k_list.reverse()
        # 读进来的数据是按时间，这里倒转，[::-1]已经倒转了，所以不用了
        flag = False
        if k_list[0]['mid'] + 0.01 >= k_list[1]['mid']:
            "判断 mid 已平"
            "N : Negative"
            "P : Passive"
            """ 这里只算了层级，后面加入差 """
            # 过滤掉 板（max、min、open和close都相等） 这种特殊K线
            for i in range(0, 8):
                k_value = k_list[0]
                if i >= 2 and not flag:
                    # 阴线计算到第几根
                    break
                if (k_value['close'] - k_value['lastclose']) < 0 and (k_value['close'] - k_value['open']) < 0:
                    first_N.append(k_value)
                    first_close.append(k_value['close'])
                    first_vol.append(k_value['volumn'])
                    flag = True
                else:
                    if flag:
                        break
                k_list.pop(0)
            # print(first_N)
            # print(len(first_N))
            flag = False
            for i in range(0, 8):
                k_value = k_list[0]
                if i >= 4 and not flag:
                    break
                if (k_value['close'] - k_value['lastclose']) < 0 and (k_value['close'] - k_value['open']) < 0:
                    second_N.append(k_value)
                    second_close.append(k_value['close'])
                    second_vol.append(k_value['volumn'])
                    flag = True
                else:
                    # passiveList.append(k_value['close'])
                    if flag:
                        break
                k_list.pop(0)
            # print(second_N)
            # first_vol = [k['volumn'] for k in first_N]
            # print(first_vol)
            # print(second_vol)
        if len(first_N) >= 1 and len(second_N) >= 1:
            if first_close[0] > second_close[0] and max(first_vol) < max(second_vol):
                boll_pos = [d for d in ((k['close'] - k['mid']) for k in s) if d < 0]
                # k['close'] - k['mid']) for k in s
                # k 是 列表s的元素，计算字典元素k的close和mid之差，构建成新的列表
                # [d for d in ((k['close'] - k['mid']) for k in s) if d < 0]
                # d是 新的列表 中 满足 d < 0的元素，然后把符合条件的结果d 构建成新的列表
                # 赋值给 boll_pos
                # 这个列表保存的就是处在布林中轨以下的 收盘价与中轨之差
                if len(boll_pos) > 0:
                    print(code)
                # print(code + '\t' + format(second_close[0], '0.2f') + '\t' + format(first_close[0], '0.2f') + '\t' +
                #       format(max(second_vol), 'd') + '\t' + format(max(first_vol), 'd'))



# 前阴连阴，连阴后必须连阳，再阴；双阴必须前低后高
# 中间的连阳可以假阳
# 前后都是连阴形态，也要考虑
# 中轨怎么考虑
# 找第一组连阴 和 第二组连阴（真阴） 以及中间的阳线