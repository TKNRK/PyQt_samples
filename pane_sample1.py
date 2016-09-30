from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from agiTest import AGI

class agiWindow(QGraphicsView):
    def __init__(self, width=500,height=500,size=5):
        super(agiWindow, self).__init__()

        self.m_scene = QGraphicsScene()
        self.setScene(self.m_scene)

        agi = AGI(width, width-100, 2)
        print(agi.Pos_scaled)
        self.width = width
        self.height = height
        self.size = size
        self.node = (agi.Pos_scaled).T
        self.edge = agi.EdgeList

        self.lines = []
        self.ellipses = []
        self.selected = 0

        self.setUp()

    def initUI(self):
        self.update()

    def setUp(self, ef = -1):
        self.m_scene.setSceneRect(0, 0, 800, 800)
        self.counter = 0

        for n in self.node:
            item = QGraphicsEllipseItem(*n, 50, 50)

            item.setPen(QPen(Qt.black, 1))
            item.setBrush(QBrush(Qt.white))

            if ef == self.counter:
                effect = QGraphicsDropShadowEffect(self)
                effect.setBlurRadius(8)
                item.setGraphicsEffect(effect)
                item.setZValue(1)

            self.m_scene.addItem(item)
            self.ellipses.append(item)


    def mousePressEvent(self, event):
        self.selected = 1
        print(self.ellipses)
        super(agiWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.node[self.selected,:] = np.array([pos.x(),pos.y()])
        self.m_scene.clear()
        self.ellipses.clear()
        self.setUp(self.selected)
        super(agiWindow, self).mouseMoveEvent(event)

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)

        # グラフ描画領域の埋め込み
        self.graphDrawer = agiWindow(800, 800)
        self.graphicsView = self.graphDrawer

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