from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from file_io import jsonFiles

import sys
import os

from fromgc.EXE.UI_20170809 import Ui_Form    # 导入生成form.py里生成的类


def myAlign(string, length=0):
    if length == 0:
        return string
    slen = len(string)
    re = string
    if isinstance(string, str):
        placeholder = '   '
    else:
        placeholder = ' '
    while slen < length:
        re += placeholder
        slen += 1
    return re


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        # self.outputRootPath = 'Z:/Test'
        self.outputRootPath = 'D:/Test'
        self.clPath = self.outputRootPath + '/strategy.json'
        self.clRead = jsonFiles.jsonRead(self.clPath)
        self.clList = list(self.clRead.keys())
        self.selectHY_Row = -1
        self.selectGN_Row = -1
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)

        # 定义槽函数
    def reload(self):
        self.clWidget.clear()
        for i in range(0, len(self.clList)):
            # print(codeList[i])
            item = QtWidgets.QListWidgetItem()
            self.clWidget.addItem(item)
            self.clWidget.item(i).setText(self.clList[i])

    def clickCL(self):
        self.tableWidget.clearContents()
        self.selectHY_Row = -1
        self.selectGN_Row = -1

    def selectCL(self):
        self.selectHY_Row = -1
        self.selectGN_Row = -1
        self.gnWidget.clear()
        self.hyWidget.clear()
        self.tableWidget.clearContents()

        self.clStr = self.clRead[self.clList[self.clWidget.currentRow()]]

        self.gnPath = self.outputRootPath + '/' + self.clStr + '/BlockResultGN.json'
        self.gnRead = jsonFiles.jsonRead(self.gnPath)
        self.gnList = list(self.gnRead.keys())
        # self.gnWidget.clear()
        for i in range(0, len(self.gnList)):
            item = QtWidgets.QListWidgetItem()
            self.gnWidget.addItem(item)
            spa = '\t'
            self.gnWidget.item(i).setText(myAlign(self.gnList[i].split('>')[-1], 21) + '(' + format(len(self.gnRead[self.gnList[i]]), '03d') + ')')

        self.hyPath = self.outputRootPath + '/' + self.clStr + '/BlockResultHY.json'
        self.hyRead = jsonFiles.jsonRead(self.hyPath)
        self.hyList = list(self.hyRead.keys())
        # self.hyWidget.clear()
        for i in range(0, len(self.hyList)):
            item = QtWidgets.QListWidgetItem()
            self.hyWidget.addItem(item)
            spa = '\t'
            self.hyWidget.item(i).setText(myAlign(self.hyList[i].split('>')[-1], 21) + '(' + format(len(self.hyRead[self.hyList[i]]), '03d') + ')')

    # http://blog.csdn.net/lainegates/article/details/8314287
    # pyqt下QTableWidget使用方法小结

    def selectHY(self):
        self.selectGN_Row = -1
        if self.selectHY_Row != self.hyWidget.currentRow():
            self.selectHY_Row = self.hyWidget.currentRow()
            hyList = self.hyRead[self.hyList[self.selectHY_Row]]
            self.tableWidget.setRowCount(len(hyList))
            i = 0
            for element in hyList:
                newItem = QTableWidgetItem(element)
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 0, newItem)
                newItem = QTableWidgetItem(" ")
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 1, newItem)
                i += 1

    def selectGN(self):
        self.selectHY_Row = -1
        if self.selectGN_Row != self.gnWidget.currentRow():
            self.selectGN_Row = self.gnWidget.currentRow()
            gnList = self.gnRead[self.gnList[self.selectGN_Row]]
            self.tableWidget.setRowCount(len(gnList))
            i = 0
            for element in gnList:
                newItem = QTableWidgetItem(element)
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 0, newItem)
                newItem = QTableWidgetItem(" ")
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(i, 1, newItem)
                i += 1

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
