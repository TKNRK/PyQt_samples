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

        self.agi = AGI(width, width-100, 2)
        self.width = width
        self.height = height
        self.size = size
        self.node = (self.agi.Pos_scaled).T
        self.edge = self.agi.EdgeList

        self.lines = []
        self.ellipses = []
        self.selected = False
        self.selection = None

        self.setUp()

    def setUp(self):
        self.m_scene.setSceneRect(0, 0, self.width, self.width)

        for e in self.edge:
            item = QGraphicsLineItem(*self.node[e[0]], *self.node[e[1]])
            item.setPen(QPen(Qt.blue, 1))
            self.m_scene.addItem(item)
            self.lines.append(item)

        for n in self.node:
            item = QGraphicsEllipseItem(*n, 50, 50)
            item.setPen(QPen(Qt.black, 1))
            item.setBrush(QBrush(Qt.white))
            self.m_scene.addItem(item)
            self.ellipses.append(item)

    def mousePressEvent(self, event):
        for i in range(15):
            if self.ellipses[i].isUnderMouse():
                self.selection = i
                self.selected = True
        super(agiWindow, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self. selected:
            pos = event.pos()
            self.agi.node_update(pos.x(), pos.y(), self.selection)
            self.m_scene.clear()
            self.ellipses.clear()
            self.lines.clear()
            self.setUp()
            super(agiWindow, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.selected:
            pos = event.pos()
            self.agi.node_update(pos.x(), pos.y(), self.selection)
            self.m_scene.clear()
            self.ellipses.clear()
            self.lines.clear()
            self.setUp()
            self.selected = False
            self.selection = None

class ParamView(QGraphicsView):
    def __init__(self, height=50,width=100,size=5):
        super(ParamView, self).__init__()

        self.p_scene = QGraphicsScene()
        self.setScene(self.p_scene)

        # パラメータを作るクラスを生成する
        #agi = AGI(width, width-100, 2)
        self.width = width
        self.height = height
        self.size = size
        self.vals = np.arange(10)
        self.bars = np.arange(10)
        self.b1 = 0
        self.b2 = len(self.bars) - 1
        self.div = len(self.bars) - 1
        
        self.lines = []
        self.rects = []
        
        self.setUp()

    def setUp(self):
        self.p_scene.setSceneRect(0, 0, self.height, self.width)
        length = self.width / self.div
        # min > 0 の場合のみ考えている
        vals_fixed = self.vals / max(self.vals) * 40

        self.b1 = 2
        self.b2 = 6

        for i in range(self.div):
            pos_x = 10 + length*(i-1)
            pos_y = 5 + (40 - vals_fixed[i])
            item = QGraphicsRectItem(pos_x,pos_y,length,vals_fixed[i])
            item.setPen(QPen(Qt.white, 1))

            if self.b1 <= i and i<= self.b2:
                item.setBrush(QBrush(Qt.black))
            else:
                item.setBrush((QBrush(Qt.gray)))

            self.p_scene.addItem(item)
            self.rects.append(item)

    def mousePressEvent(self, event):
        for i in range(self.div):
            if self.rects[i].isUnderMouse():
                if i <= self.b1: self.b1 = i
                else : self.b2 = i
                print("clicked")
        print(self.b1)
        print(self.b2)
        self.p_scene.clear()
        self.rects.clear()
        self.setUp()
        super(ParamView, self).mousePressEvent(event)

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)

        # グラフ描画領域の埋め込み
        self.graphicsView = agiWindow(800, 800)
        
        # パラメータ領域の埋め込み
        self.nullButton1 = QPushButton("&NULL1")
        self.nullButton1.clicked.connect(self.do_nothing)
        self.paramView1 = ParamView(50,100)
        self.nullButton2 = QPushButton("&NULL2")
        self.nullButton2.clicked.connect(self.do_nothing)
        self.paramView2 = ParamView(50,100)
        ParamLayout = QVBoxLayout()
        ParamLayout.addWidget(self.nullButton1)
        ParamLayout.addWidget(self.paramView1)
        ParamLayout.addWidget(self.nullButton2)
        ParamLayout.addWidget(self.paramView2)

        # 文字列出力領域の埋め込み
        self.outPutLine = QLineEdit()
        self.outPutLine.setReadOnly(True)
        self.outPutLine.setText("Show ClickedNodeID")
        self.outPutLine.setText("Show Neighbors")
        TextLayout = QVBoxLayout()
        TextLayout.addWidget(self.outPutLine)

        # BoxLayout
        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(ParamLayout)
        propertyLayout.addLayout(TextLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        # その他処理
        self.setLayout(mainLayout)
        self.setWindowTitle("Social Viewpoint Finder")

    #def keyPressEvent(self,event)
    #    key = event.key()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def do_nothing(self):
        return 0


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())