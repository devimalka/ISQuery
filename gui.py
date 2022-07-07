
from concurrent.futures import thread
from email.mime import base
import threading
import traceback
from unittest import result
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QPushButton,QLabel,QCheckBox,QBoxLayout,QVBoxLayout,QHBoxLayout,QPlainTextEdit,QLineEdit,QMessageBox,QComboBox,QRadioButton
from PyQt5.QtGui import QPalette,QColor,QIcon,QFont
from PyQt5.QtCore import pyqtSlot,QObject,QThread,pyqtSignal,QRunnable,QThreadPool
import os
from threading import *
import sys
basedir = os.path.dirname(__file__)
from sqlalchemy import true



from Main import *
from MyLib import *
from env import *
from Queries import *


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

    
class Worker(QThread):
    def __init__(self,query,filename,choices,fileExtension,iterativeornot):
        super(Worker,self).__init__()
        self.signals = WorkerSignals()
        self.query =query
        self.filename = filename
        self.choices = choices
        self.fileExtension = fileExtension
        self.iterativeornot =iterativeornot
   

    @pyqtSlot()
    def run(self):
        SaveToExcel(self.query,self.filename,self.choices,self.fileExtension,self.iterativeornot)
  
           

class AnotherWindow(QWidget):
    
    def __init__(self,windowname):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.setWindowTitle(windowname)
        self.setWindowIcon(QIcon(os.path.join(basedir,'./images/import.png')))
        self.setFixedSize(460,440)
        self.layout.addWidget(self.label)
        
        # Query
        self.textinput = QPlainTextEdit()
        self.layout.addWidget(self.textinput)
        
        self.qhboxlayout1 = QHBoxLayout()
        self.IterativeRadiobtn1 = QRadioButton('All Locations')
        self.IterativeRadiobtn2 = QRadioButton('Current Locations')
        self.IterativeRadiobtn2.setChecked(True)
       
        self.qhboxlayout1.addWidget(self.IterativeRadiobtn1)
        self.qhboxlayout1.addWidget(self.IterativeRadiobtn2)
        
        self.layout.addLayout(self.qhboxlayout1)
        
        # Check boxes
        self.c1 = QCheckBox("sc",self)
        self.c2 = QCheckBox("ad",self)
        self.c3 = QCheckBox("sr",self)
        self.c4 = QCheckBox("fc",self)
        
        self.hboxlayoutchoices = QHBoxLayout()
        
    
        #adding checkboxes to layout
        self.checkboxlist = [self.c1,self.c2,self.c3,self.c4]
        for cbox in self.checkboxlist:
            self.hboxlayoutchoices.addWidget(cbox)
        self.layout.addLayout(self.hboxlayoutchoices)

        # filename 
        self.filename = QLineEdit()
        self.layout.addWidget(self.filename)
            
        # Combo box to show the filetype which need to be saved
        self.extensions = QComboBox()
        self.combodict = {'Excel 97-2003 Workbook (*.xls)':'xls','CSV UTF-8 (Comma delimited) (*.csv)':'csv'}
        self.extensions.addItems(self.combodict)
        self.layout.addWidget(self.extensions)
        
        # import button
        self.exportBtn = QPushButton('Import')
        self.layout.addWidget(self.exportBtn)    
        
        #import function when button clicked  
        self.exportBtn.clicked.connect(self.importExcel)   
        
        #setting layout
        self.setLayout(self.layout)
      
    def closeEvent(self,event):
        close = QMessageBox.question(self,"QUIT","Are you sure want to stop process?",
                                     QMessageBox.Yes|QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
            self.worker.quit()
        else:
            event.ignore()
    
    def RadioButtonCheck(self):
        if self.IterativeRadiobtn1.isChecked():
            return True
        if self.IterativeRadiobtn2.isChecked():
            return False
        
    
    def setWidgetsDisableorEnable(self,widgetlist,DisabledOrEnabled):
        
        for widget in widgetlist:
            widget.setEnabled(DisabledOrEnabled)

    def importExcel(self):
        self.cboxlist = []
        for cbox in self.checkboxlist:
            if cbox.isChecked():
                self.cboxlist.append(cbox.text())
        
        self.textinput.setReadOnly(True)
        self.filename.setReadOnly(True)
        
        self.setWidgetsDisableorEnable([self.exportBtn,self.extensions],False)
        self.setWidgetsDisableorEnable(self.findChildren(QCheckBox),False)
        self.setWidgetsDisableorEnable(self.findChildren(QRadioButton),False)
        
        self.saveFilename = self.filename.text()
        self.text = self.textinput.toPlainText()
        self.inputextension = self.extensions.currentText()
        self.getvalue = self.combodict.get(self.inputextension)
        self.truorfalse = self.RadioButtonCheck()

        self.worker = Worker(self.text,self.saveFilename,self.cboxlist,self.getvalue,self.truorfalse)
        self.worker.finished.connect(self.complete)
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
        self.setWindowIcon(QIcon(os.path.join(basedir,'./images/window_icon.png')))
        self.setFixedSize(360,360)

        #create qwidget because can't add qlayout to mainwindow
        self.wid = QWidget()

        #set qwidget as centralwidget
        self.setCentralWidget(self.wid)
        
        #create layout
        self.layout = QVBoxLayout()
        self.button2 = QPushButton('Query Import')
        self.button2.setFont(QFont('SansSerif',10))
        self.layout.addWidget(self.button2,2)
        self.button2.clicked.connect(self.runBtn)
        
        #add layout to central widget
        self.wid.setLayout(self.layout)

    def runBtn(self):
           self.button2.setDisabled(True)
           self.w = AnotherWindow('Query Import')
           self.w.show()

     

app = QApplication([])
app.processEvents()
window = MainWindow()
window.show()

app.exec()