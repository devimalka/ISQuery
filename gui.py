
from concurrent.futures import thread
import threading
import traceback
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QPushButton,QLabel,QCheckBox,QBoxLayout,QVBoxLayout,QHBoxLayout,QPlainTextEdit,QLineEdit,QMessageBox,QComboBox,QRadioButton
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import pyqtSlot,QObject,QThread,pyqtSignal,QRunnable,QThreadPool

from threading import *
import sys

from sqlalchemy import true



from Main import *
from MyLib import *
from env import *
from Queries import *




           

class AnotherWindow(QWidget):
    
    def __init__(self,windowname):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.setWindowTitle(windowname)
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
        self.exportBtn.clicked.connect(self.IMPORT)   
        
        #setting layout
        self.setLayout(self.layout)
    
    def RadioButtonCheck(self):
        if self.IterativeRadiobtn1.isChecked():
            return True
        if self.IterativeRadiobtn2.isChecked():
            return False
        
        

    def IMPORT(self):
        self.cboxlist = []
        for cbox in self.checkboxlist:
            if cbox.isChecked():
                self.cboxlist.append(cbox.text())
        self.textinput.setReadOnly(True)
        self.filename.setReadOnly(True)
        
        self.exportBtn.setDisabled(True)    
        self.saveFilename = self.filename.text()
        self.text = self.textinput.toPlainText()
        self.inputextension = self.extensions.currentText()
        self.getvalue = self.combodict.get(self.inputextension)
        self.truorfalse = self.RadioButtonCheck()
       
        self.queryThread = threading.Thread(target=SaveToExcel,args=(self.text,self.saveFilename,self.cboxlist,self.getvalue,self.truorfalse))
        self.queryThread.start()
       
       
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
app.processEvents()
window = MainWindow()
window.show()

app.exec()