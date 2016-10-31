import math
import random
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Sample(QGraphicsView):
    def __init__(self, parent=None):
        super(Sample, self).__init__(parent)

        self.m_scene = QGraphicsScene()
        self.ellipses = []
        self.setScene(self.m_scene)

        self.isSelected = False
        self.selection = None

        self.setupScene()

    def setupScene(self):
        self.m_scene.setSceneRect(0, 0, 800, 800)

        for i in range(3):
            item = QGraphicsEllipseItem(0, 0, 50, 50)

            item.setPen(QPen(Qt.black, 1))
            if i == 0: item.setBrush(QBrush(Qt.blue))
            if i == 1: item.setBrush(QBrush(Qt.yellow))
            if i == 2: item.setBrush(QBrush(Qt.red))

            item.setPos(random.randint(100,600), random.randint(100,600))
            self.m_scene.addItem(item)
            self.ellipses.append(item)


    def mousePressEvent(self, event):
        # line1 = QGraphicsLineItem(x-3, y, x+3, y)
        # line2 = QGraphicsLineItem(x, y+3, x, y-3)
        # self.m_scene.addItem(line1)
        # self.m_scene.addItem(line2)

        for i in range(self.agi.node_num):
            if self.ellipses[i].isUnderMouse():
                self.selection = i
                self.isSelected = True
                effect = QGraphicsDropShadowEffect(self)
                effect.setBlurRadius(20)
                if i==0:effect.setColor(Qt.blue)
                elif i==1:effect.setColor(Qt.yellow)
                else : effect.setColor(Qt.red)
                effect.setOffset(QPointF(self.ellipses[i].pos()))
                self.ellipses[i].setGraphicsEffect(effect)
        super(Sample, self).mousePressEvent(event)

    def mousePressEvent(self, QMouseEvent):
        print("")

    def mouseReleaseEvent(self, QMouseEvent):
        print("")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    sample = Sample()
    sample.setWindowTitle("sample")
    sample.resize(800, 800)
    sample.show()

    sys.exit(app.exec_())
