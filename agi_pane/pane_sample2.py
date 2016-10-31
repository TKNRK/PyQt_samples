from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
import numpy as np
from agiTest import AGI

class AGIwindow(QGraphicsItem):
    def __init__(self, width=500,height=500,size=5):
        super(AGIwindow, self).__init__()
        agi = AGI(width, width-100, 2)
        print(agi.Pos_scaled)
        self.width = width
        self.height = height
        self.size = size
        self.node = (agi.Pos_scaled).T
        self.edge = agi.EdgeList
        self.initUI()

    def initUI(self):
        self.update()

    def paint(self, painter, optinon, widget):
        painter.setPen(QColor(220,220,220))
        for e in self.edge:
            painter.drawLine(*self.node[e[0],:],*self.node[e[1],:])

        painter.setBrush(Qt.black)
        for n in self.node:
            painter.drawEllipse(*(n - 5),10,10)

    """
    def mousePressEvent(self, event):
        pos = event.pos()
        self.select(int(pos.x() / 100), int(pos.y() / 100))
        self.update()
        super(AGIwindow, self).mousePressEvent(event)
    """

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)

        # グラフ描画領域の埋め込み
        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0,0,800,800)
        self.graphicsView.setScene(scene)
        self.graphDrawer = AGIwindow(800, 800)
        scene.addItem(self.graphDrawer)

        # パラメータ領域の埋め込み
        self.nullButton1 = QPushButton("&NULL1")
        self.nullButton1.clicked.connect(self.do_nothing)
        self.nullButton2 = QPushButton("&NULL2")
        self.nullButton2.clicked.connect(self.do_nothing)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.nullButton1)
        buttonLayout.addWidget(self.nullButton2)

        # 文字列出力領域の埋め込み
        #textLayout = QHBoxLayout
        #textLayout.addWidget(QLabel("Text"))
        #textLayout.addWidget(QLineEdit())

        # BoxLayout
        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(buttonLayout)
        #propertyLayout.addLayout(textLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        # その他処理
        self.setLayout(mainLayout)
        self.setWindowTitle("Social Viewpoint Finder")

    # 関数定義
    def do_nothing(self):
        self.update()

    def zero(self):
        return 0


    #def keyPressEvent(self,event)
    #    key = event.key()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())