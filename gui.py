
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QPushButton,QLabel,QCheckBox,QBoxLayout,QVBoxLayout,QHBoxLayout,QPlainTextEdit,QLineEdit,QMessageBox
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import pyqtSlot,QObject,QThread,pyqtSignal

import sys

from sqlalchemy import true



from Main import *


class workerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QThread):
    def __init__(self,query,filename):
        super(Worker,self).__init__()
        self.signals = workerSignals()
        self.query =query
        self.filename = filename
        
        
    @pyqtSlot()
    def run(self):
        try:
            saveToExcel(self.query,self.filename)
        except:
            self.signals.result.emit(self.signals.result)
        finally:
            self.signals.finished.emit()
   


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
        
        self.exportBtn = QPushButton('Import')
        self.layout.addWidget(self.exportBtn)
        
        self.exportBtn.clicked.connect(self.IMPORT)
        
        
        
        
        
        self.setLayout(self.layout)
        
        
    def IMPORT(self):
        
        self.textinput.setReadOnly(True)
        self.filename.setReadOnly(True)
        
        self.exportBtn.setDisabled(True)    
        self.saveFilename = self.filename.text()
        self.text = self.textinput.toPlainText()

        self.worker = Worker(self.text,self.saveFilename)
        self.worker.signals.finished.connect(self.complete)
        self.worker.start()
       
       
    def complete(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Status")
        self.msg.setText("Import Done")
        self.msg.exec()
        self.textinput.setReadOnly(False)
        self.filename.setReadOnly(False)
        self.exportBtn.setDisabled(False)
        self.exportBtn.setText("Import Again")
       



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

        # self.button = QPushButton()
        # self.button.setText("Doc Tally")
        # self.layout.addWidget(self.button)
        # self.button.clicked.connect(self.runBtn)


        self.button2 = QPushButton('Query Import')
        self.layout.addWidget(self.button2,2)
        self.button2.clicked.connect(self.runBtn)
        

        #add layout to central widget
        self.wid.setLayout(self.layout)

    def runBtn(self):
           self.button2.setDisabled(True)
           self.w = AnotherWindow('Query Import')
           self.w.show()

     

app = QApplication([])

window = MainWindow()
window.show()

app.exec()