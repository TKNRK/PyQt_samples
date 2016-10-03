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

    def setUp(self, ef = -1):
        self.m_scene.setSceneRect(0, 0, self.width, self.width)
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

class ParamView(QGraphicsView):
    def __init__(self, width=100,height=50,size=5):
        super(ParamView, self).__init__()

        self.p_scene = QGraphicsScene()
        self.setScene(self.p_scene)

        # パラメータを作るクラスを生成する
        #agi = AGI(width, width-100, 2)
        self.width = width
        self.height = height
        self.size = size
        self.vals = np.array([1.2,0.3,4.0,2.8])
        self.bars = np.array([0,1,2,3,4])
        
        self.lines = []
        self.rects = []
        
        self.setUp()

    def setUp(self):
        self.p_scene.setSceneRect(0, 0, 100, 50)
        self.counter = 0
        div = len(self.bars) - 1
        length = self.width / div
        # min > 0 の場合のみ考えている
        vals_fixed = self.vals / max(self.vals) * 40

        for i in range(div):
            pos_x = 10 + length*(i-1)
            pos_y = 5 + (40 - vals_fixed[i])
            item = QGraphicsRectItem(pos_x,pos_y,length,vals_fixed[i])

            item.setPen(QPen(Qt.black, 1))
            item.setBrush(QBrush(Qt.white))

            self.p_scene.addItem(item)
            self.rects.append(item)


class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)

        # グラフ描画領域の埋め込み
        self.graphicsView = agiWindow(800, 800)
        
        # パラメータ領域の埋め込み
        self.nullButton1 = QPushButton("&NULL1")
        self.nullButton1.clicked.connect(self.do_nothing)
        self.paramView1 = ParamView()
        self.nullButton2 = QPushButton("&NULL2")
        self.nullButton2.clicked.connect(self.do_nothing)
        self.paramView2 = ParamView()
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.nullButton1)
        buttonLayout.addWidget(self.paramView1)
        buttonLayout.addWidget(self.nullButton2)
        buttonLayout.addWidget(self.paramView2)

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