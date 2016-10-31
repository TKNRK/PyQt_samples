from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ClickView(QGraphicsView):

    number = 0

    def __init__(self, parent=None):
        super(ClickView, self).__init__(parent)
        self.m_scene = QGraphicsScene()
        self.ellipse = None
        self.setScene(self.m_scene)
        self.setupScene()

    def setupScene(self):
        self.m_scene.setSceneRect(0, 0, 100, 100)

        item = QGraphicsEllipseItem(25, 25, 50, 50)
        item.setPen(QPen(Qt.black, 1))
        item.setBrush(QBrush(Qt.blue))
        self.m_scene.addItem(item)
        self.ellipse = item

    def mousePressEvent(self, event):
        ClickView.number += 1
        if self.ellipse.isUnderMouse():
            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(20)
            effect.setColor(Qt.blue)
            effect.setOffset(QPointF(self.ellipse.pos()))
            self.ellipse.setGraphicsEffect(effect)
        super(ClickView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        print("")
        super(ClickView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.ellipse.isUnderMouse():
            self.ellipse.setGraphicsEffect(None)
        super(ClickView, self).mouseReleaseEvent(event)

class QB(QTextEdit):
    def __init__(self, parent = None):
        super(QB,self).__init__(parent)

        self.c = ClickView()

    def rewrite(self,bool):
        self.append(str(self.c.number))

class Sample(QWidget):
    def __init__(self, parent = None):
        super(Sample, self).__init__(parent)

        self.view = ClickView()
        self.text = QB()
        self.b = QPushButton("&update")

        p = QVBoxLayout()
        p.setAlignment(Qt.AlignTop)
        p.addWidget(self.b)
        p.addWidget(self.text)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.view)
        mainLayout.addLayout(p)

        self.setLayout(mainLayout)
        self.setWindowTitle("Social Viewpoint Finder")

        self.b.clicked.connect(self.text.rewrite)

    def something(self,e):
        print("ok")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Q: self.close()
        if key == Qt.Key_Escape: self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    sample = Sample()
    sample.setWindowTitle("sample")
    sample.resize(200, 200)
    sample.show()

    sys.exit(app.exec_())
