from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys
import os
import time
import webbrowser

from gui.hello import Ui_Form    # 导入生成form.py里生成的类


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

tempPath = 'z:/test/codeList.txt'
codeList = None
if os.path.exists(tempPath):
    print('file is exist.')
    f = open(tempPath, 'r')
    text = f.read()
    f.close()
    codeList = text.splitlines()
    codeList.sort()
    # codeList = codeList[0:2]


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    # 定义槽函数
    def hello(self):
        self.listWidget.clear()
        for i in range(0, len(codeList)):
            # print(codeList[i])
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
            self.listWidget.item(i).setText(codeList[i])

    def selectCode(self):
        code = codeList[self.listWidget.currentRow()]
        nowTime = get_time_stamp()
        self.textEdit.setText(code)
        self.tableWidget.item(0, 0).setText(code)
        self.tableWidget.item(1, 0).setText(nowTime)

        code_text = 'sh000001'

        if code[0] == '6':
            code_text = 'sh' + code
        elif code[0] == '0' or code[0] == '3':
            code_text = 'sz' + code
        gifLink = 'http://image.sinajs.cn/newchart/daily/n/' + code_text + '.gif'
        webbrowser.open(gifLink)
        # gif = QtGui.QImage()
        # gif.load(gifLink)
        # print(gif)

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
