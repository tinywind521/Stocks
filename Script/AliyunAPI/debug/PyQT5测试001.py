# -*- coding:utf8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SingleNote(QGraphicsTextItem):
    def __init__(self, parent=None, scene=None):
        super(SingleNote, self).__init__(parent, scene)
        self.setHtml("<strong>Hello</strong>")

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.scale(2.0, 2.0)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        QGraphicsSceneHoverEvent.ignore()

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.scale(0.5, 0.5)

class NoteScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(NoteScene, self).__init__(parent)

class MainView(QGraphicsView):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mv = MainView()
    scene = NoteScene()
    item = SingleNote()
    scene.addItem(item)
    mv.setScene(scene)
    mv.show()
    app.exec_()