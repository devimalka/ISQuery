
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QPushButton,QLabel,QCheckBox,QBoxLayout,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPalette,QColor


import sys

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        
        self.setFixedSize(360,360)


        layout = QVBoxLayout()
        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))

        layout2 = QHBoxLayout()
        layout2.addWidget(Color('blue'))
        layout2.addWidget(Color('black'))

        layout.addLayout(layout2)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

  

app = QApplication([])

window = MainWindow()
window.show()

app.exec()