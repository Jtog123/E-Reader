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

        label = QLabel("THIS IS AWESOME")
        label.setAlignment(Qt.AlignCenter)

        #Create a toolbar add button and widgets to the toolbar
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)
        self.setCentralWidget(label)

        button_action = QAction(QIcon("icons/bug.png"),"Button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        button_action.setShortcut( QKeySequence("Ctrl+p") )
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("icons/balance.png"), "Button 2", self)
        button_action2.setStatusTip("This is your second button")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())


        self.setStatusBar(QStatusBar(self))
        
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action) 
        file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action2)   

        
    
    def onMyToolBarButtonClick(self, s):
        print("click", s)



#only one instance
app = QApplication(sys.argv)

window = MainWindow()
window.show()


# Start the event loop
app.exec_()