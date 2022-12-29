from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()

        self.setWindowTitle("My awesome app")

        label = QLabel("THIS IS AWESOME")
        
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)


#only one instance
app = QApplication(sys.argv)

window = MainWindow()
window.show()


# Start the event loop
app.exec_()