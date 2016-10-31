import math

from PyQt5.QtCore import QPointF, Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPen, QPainter,
                         QPixmap, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView)


class Lighting(QGraphicsView):
    def __init__(self, parent=None):
        super(Lighting, self).__init__(parent)

        self.angle = 0.0
        self.m_scene = QGraphicsScene()
        self.m_items = []

        self.setScene(self.m_scene)

        self.setupScene()

        self.flag = True


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Q: self.close()
        if key == Qt.Key_Escape: self.close()

    def setupScene(self):
        self.m_scene.setSceneRect(-300, -200, 600, 460)

        for i in range(-2, 3):
            for j in range(-2, 3):
                if (i + j) & 1:
                    item = QGraphicsEllipseItem(0, 0, 50, 50)
                    item.setPen(QPen(Qt.lightGray, 0))
                    item.setBrush(QBrush(Qt.lightGray))
                else:
                    item = QGraphicsRectItem(0, 0, 50, 50)
                    item.setPen(QPen(Qt.black, 0))
                    item.setBrush(QBrush(Qt.black))

                effect = QGraphicsDropShadowEffect(self)
                effect.setBlurRadius(8)
                item.setGraphicsEffect(effect)
                item.setZValue(1)
                item.setPos(i * 80, j * 80)
                self.m_scene.addItem(item)
                self.m_items.append(item)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    lighting = Lighting()
    lighting.setWindowTitle("Lighting and Shadows")
    lighting.resize(640, 480)
    lighting.show()

    sys.exit(app.exec_())