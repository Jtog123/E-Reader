from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()


        #one window title chaged triggers all those functions to go off
        #after executing htey return and go back
        self.setWindowTitle("My awesome app")



        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        widget.currentIndexChanged.connect(self.index_changed)
        widget.currentIndexChanged[str].connect(self.text_changed)

        self.setCentralWidget(widget)

    def index_changed(self, i):
        print(i)
    
    def text_changed(self, s):
        print(s)




#only one instance
app = QApplication(sys.argv)

window = MainWindow()
window.show()


# Start the event loop
app.exec_()