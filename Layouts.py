from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
        super(MainWindow, self).__init__()


        #one window title chaged triggers all those functions to go off
        #after executing htey return and go back
        self.setWindowTitle("My awesome app")

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)

        for n, color in enumerate(['red','green','blue','yellow']):
            tabs.addTab(Color(color), color)
        
        self.setCentralWidget(tabs)





#only one instance
app = QApplication(sys.argv)

window = MainWindow()
window.show()


# Start the event loop
app.exec_()