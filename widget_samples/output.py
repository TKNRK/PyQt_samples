import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QWidget):
    def __init__(self, icon, parent=None):
        super(MainWindow, self).__init__(parent)

        self.outputLine = QTextEdit()
        self.outputLine.setReadOnly(True)

        self.messages = ["Good","Relatively Good","So-So","Relatively Bad","Bad"]
        self.data = []

        self.buttons = []
        for i in range(5):
            self.buttons.append(QPushButton("N:"+str(i)))
            self.buttons[i].clicked.connect(self.calc)

        self.del_button = QPushButton()
        self.del_button.setIcon(icon)
        self.del_button.clicked.connect(self.back)

        buttonLayout = QHBoxLayout()
        for b in self.buttons:
            buttonLayout.addWidget(b)
        buttonLayout.addWidget(self.del_button)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(QLabel("push the button"))
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(QLabel("result:"))
        mainLayout.addWidget(self.outputLine)

        self.setLayout(mainLayout)
        self.setWindowTitle("Factorial")

    def calc(self):
        for i in range(len(self.buttons)):
            if self.buttons[i].underMouse():
                m = self.messages[i]
                self.outputLine.append(m)
                self.data.append(i)

    def back(self):
        self.data.remove(len(self.data) - 1)
        self.outputLine.clear()
        for d in self.data:
            self.outputLine.append(self.messages[d])

    def save_result(self):
        self.outputLine.clear()
        np.savetxt("eval.csv",self.data,fmt="%d")
        self.data.clear()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Q: self.close()
        if key == Qt.Key_S: self.save_result()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    style = app.style()
    icon = style.standardIcon(QStyle.StandardPixmap(QStyle.SP_FileDialogBack))
    main_window = MainWindow(icon)

    main_window.show()
    sys.exit(app.exec_())