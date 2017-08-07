from PyQt5 import QtWidgets, QtGui, QtCore

import sys, os

from gui.hello import Ui_Form    # 导入生成form.py里生成的类

tempPath = 'z:/test/codeList.txt'
codeList = None
if os.path.exists(tempPath):
    print('file is exist.')
    f = open(tempPath, 'r')
    text = f.read()
    f.close()
    codeList = text.splitlines()
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
            self.listWidget.item(i).setText(QtCore.QCoreApplication.translate('Form', codeList[i]))

    def selectCode(self):
        self.textEdit.setText(codeList[self.listWidget.currentRow()])

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
