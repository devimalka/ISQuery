
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QPushButton,QLabel,QCheckBox,QBoxLayout,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import pyqtSlot

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        
        self.setFixedSize(360,360)

        #create qwidget because can't add qlayout to mainwindow
        self.wid = QWidget()

        #set qwidget as centralwidget
        self.setCentralWidget(self.wid)
        
        #create layout
        self.layout = QVBoxLayout()

        self.button = QPushButton()
        self.button.setText("Doc Tally")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.doctally)


        self.button2 = QPushButton('btn2')
        self.layout.addWidget(self.button2,2)
        self.button2.clicked.connect(self.doctally)

        #add layout to central widget
        self.wid.setLayout(self.layout)

    def doctally(self):
            self.w = QWidget()
            self.w.label = QLabel("test")
            self.w.show()

     

app = QApplication([])

window = MainWindow()
window.show()

app.exec()