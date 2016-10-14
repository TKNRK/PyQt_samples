import math
import random
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Sample(QGraphicsView):
    def __init__(self, parent=None):
        super(Sample, self).__init__(parent)

        self.angle = 0.0
        self.m_scene = QGraphicsScene()
        self.m_items = []
        self.v = [random.randint(1,20) for i in range(25)]

        self.setScene(self.m_scene)

        self.setupScene()

        timer = QTimer(self)
        timer.timeout.connect(self.animate)
        timer.setInterval(60)
        timer.start()

        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)

    def setupScene(self):
        self.m_scene.setSceneRect(0, 0, 800, 800)

        for i in range(10):
            item = QGraphicsEllipseItem(0, 0, 50, 50)

            item.setPen(QPen(Qt.black, 1))
            item.setBrush(QBrush(Qt.white))

            item.setPos(random.randint(100,600), random.randint(100,600))
            self.m_scene.addItem(item)
            self.m_items.append(item)

    def animate(self):
        self.angle += (math.pi / 30)

        for i in range(10):
            item = self.m_items[i]
            pos = item.pos()
            x = pos.x() + 5*math.sin(self.angle * self.v[i])
            y = pos.y() + 5*math.sin(self.angle * self.v[i])
            item.setPos(x,y)

        self.m_scene.update()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    sample = Sample()
    sample.setWindowTitle("sample")
    sample.resize(800, 800)
    sample.show()

    sys.exit(app.exec_())
