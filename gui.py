#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QLabel,QLineEdit,QVBoxLayout,QTextEdit
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
  
)


import sys


class Anotherwindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(220,120)
        self.label = QLabel("Another window")
        layout.addWidget(self.label)
        self.setLayout(layout)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = Anotherwindow()

        self.setWindowTitle("IS Query Exporter")
        self.setFixedSize(400,380)

        self.btn = QPushButton(self)
        self.btn.setText("push me")
        
        self.btn.clicked.connect(self.w.show)

        self.btn2 = QPushButton(self)
        self.btn2.setText("button 2")
        self.btn2.move(0,40)



app = QApplication([])

window = MainWindow()
window.show()

app.exec()