from functions import function


def get_dateList(beginDay, getLength, appcode='c7689f18e1484e9faec07122cc0b5f9e'):
    """
    截取指定长度的日起序列
    :param beginDay:
    :param getLength: 所需日期长度
    :param appcode:
    :return:
    """
    # beginDay = input('Enter beginDay: ')
    # getLength = int(input("Enter day's length: "))
    # appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
    dateList = function.return_date(beginDay, appcode)
    # print(dateList)
    if getLength < len(dateList):
        dateList = dateList[-getLength:]
    # print(dateList)
    return dateList
