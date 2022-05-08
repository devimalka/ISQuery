from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize,Qt


import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IS RPD")
        button = QPushButton("Press me")

        self.setCentralWidget(button)

        self.setFixedSize(QSize(800,600))
        #setMinimumSize
        #setMaximumSize

app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()