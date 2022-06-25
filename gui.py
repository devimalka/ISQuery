
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QPushButton,QLabel,QCheckBox,QBoxLayout,QVBoxLayout,QHBoxLayout,QPlainTextEdit,QLineEdit
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import pyqtSlot

import sys


from connector import *


class AnotherWindow(QWidget):
    
    def __init__(self,windowname):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.setWindowTitle(windowname)
        self.setFixedSize(460,440)
        self.layout.addWidget(self.label)
        
        self.textinput = QPlainTextEdit()
        self.layout.addWidget(self.textinput)

        self.filename = QLineEdit()
        self.layout.addWidget(self.filename)
        
        self.exportBtn = QPushButton('Export')
        self.layout.addWidget(self.exportBtn)
        
        self.exportBtn.clicked.connect(self.Export)
        
        
        
        
        
        self.setLayout(self.layout)
        
        
    def Export(self):
        self.exportBtn.setDisabled(True)    
        self.saveFilename = self.filename.text()
        self.text = self.textinput.toPlainText()
        # saveToExcel(self.text,)
        saveToExcel(self.text,self.saveFilename)    
       



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


        self.button2 = QPushButton('Query Export')
        self.layout.addWidget(self.button2,2)
        self.button2.clicked.connect(self.doctally)

        #add layout to central widget
        self.wid.setLayout(self.layout)

    def doctally(self):
           self.w = AnotherWindow('Query Export')
           self.w.show()

     

app = QApplication([])

window = MainWindow()
window.show()

app.exec()