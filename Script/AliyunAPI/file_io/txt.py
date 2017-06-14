import sys

from aliyun import aliyun_api


def txt_write(text, path):
    """写入指定路径的文本文档"""
    try:
        f = open(path, 'w')
        f.write(text)
        f.close()
    except ValueError:
        pass

#    f = open(path, 'w')
#    f.write(text)
#    f.close()


def txt_read(path):
    """打开指定路径的文本文档"""
    try:
        f = open(path, 'r')
        text = f.read()
        f.close()
       
        if text:
            return text
        else:
            return None
       
    except ValueError:
        pass


# def savefile(code, beginday, timetype, path, appcode):
    #   beginday = '20170101'
    #   code = input("Please enter code:")
    #   beginDay = input("Please enter beginDay:")
    #   timeType = input("Please enter beginDay:")
    #   timetype = '60'
    #   path = input("Please enter path:")
    #   path = tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件','.*'),('文本文件','.txt')])
    #   path = 'Z:/Test/60F/' + code + '.txt'
    #   appcode = 'c7689f18e1484e9faec07122cc0b5f9e'
#    qtype = 'bfq'
#    text = aliyun_api.realtime(code, beginday, timetype, qtype, appcode)
#   txt_write(text, path)
