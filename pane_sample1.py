import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np

class DrawWidget(QWidget):

    def __init__(self):
        super().__init__()
        #self.px = None
        #self.py = None
        #self.points = []
        #self.psets = []
        self.initUI()
        
    def initUI(self):
        self.setGeometry(500,500,280,270) # 引数(x,y,w,h):(出現位置,幅,高さ)
        self.setWindowTitle('Drawing Pane')
        # self.show()
    """
    def mousePressEvent(self, event):
        self.points.append(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        self.points.append(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.psets.append(event.points)
        self.points = []
        self.update()
    """
    def paintEvent(self, e):
        node = np.array([
            [0,0],
            [10,60],
            [10,160],
            [10,210],
            [10,260]
        ])
        edge = np.array([
            [0, 1],
            [0, 2],
            [1, 2],
            [1, 4],
            [3, 4]
        ])
        qp = QPainter()
        qp.begin(self)
        self.drawGraph(qp, edge, node)
        qp.end()


    def drwaGraph(self, qp, edge, node):
        self.drawLines(qp, edge, node)
        self.drawEllipses(qp, node)


    def drawLines(self, qp, edge, node):
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        # pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        for e in edge:
            qp.drawLine(*node[e[0],:],*node[e[1],:]) # 引数(x1,y1,x2,y2) : (x1,y1)から(x2,y2)のラインを引く

    def drawEllipses(selfself, qp, node):
        brush = QBrush(Qt.SolidPattern)

        #brush.setStyle(Qt.Dense1Pattern)
        qp.setBrush(brush)
        for n in node:
            qp.drawEllipse(*n, 20, 20) # 引数(x,y,w,h) : （左上座標,幅,高さ）となる矩形に内接する円


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.inputLine = QLineEdit()
        self.outputLine = QLineEdit()
        self.outputLine.setReadOnly(True)

        self.drawingP = DrawWidget

        lineLayout = QGridLayout()
        lineLayout.addWidget(QLabel("num"), 0, 0)
        lineLayout.addWidget(self.inputLine, 0, 1)
        lineLayout.addWidget(QLabel("result"), 1, 0)
        lineLayout.addWidget(self.outputLine, 1, 1)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.drawingP)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(lineLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Factorial")

    def calc(self):
        n = int(self.inputLine.text())
        r = 0
        self.outputLine.setText(str(r))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())