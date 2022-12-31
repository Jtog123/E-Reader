from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

import sys
import os



class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Set height of the window
        width = 800
        height = 800
        self.setMinimumSize(width, height)


    
        #need to be class variable or local?
        self.button_action = QAction(QIcon('icons/folder-horizontal-open.png'), 'Open File', self)
        self.button_action.triggered.connect(self.readFile)

        #Create menu bar at top of screen
        self.menu = self.menuBar()
        fileMenu = self.menu.addMenu('&File')
        fileMenu.addAction(self.button_action)

        #create button that opens file dialog
        self.button = QPushButton("&Open File", self)
        self.button.clicked.connect(self.readFile)
        self.button.move(0,200)
        
        
        
        #have the PDF file open in the window with open file
        self.webView = QWebEngineView()
        #self.webView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        #self.webView.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        #Tab Widgets
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)

        #Close Tabs
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
            #self.button.show() SHOW BUTTON AFTER TAB IS CLOSED?

        #Corner tab button
        self.tabPlus = QToolButton(self)
        self.tabPlus.setText('+')
        self.tabs.setCornerWidget(self.tabPlus)
        self.tabPlus.clicked.connect(self.readFile)


        ###### ACTUALLY KIND OF WORKS

        #Layout allows for multiple widgets to be active at once
        #probably a good idea to set this up first before adding other widgets

        layout = QVBoxLayout()

        # Add the self.tabs widget and self.button to the layout
        layout.addWidget(self.tabs)
        layout.addWidget(self.button)

        # Create a widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget of the main window to be the widget holding the layout
        self.setCentralWidget(central_widget)



    #Read files
    def readFile(self):

        #self.tabs.setCurrentWidget(self.webView)
        #self.button.hide() HIDE AND SHOW BUTTON ON CLICK
        fname = QFileDialog.getOpenFileName(self, "Open File", "c:\\", "PDF Files (*.pdf)")
        fnameString = str(fname[0])
        if fnameString != '':
            self.add_new_tab(fnameString)
            
            


    #Add Tabs
    def add_new_tab(self, fname):

        #Create a new Webview for every tab and enable settings
        view = QWebEngineView()
        view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        #self.setCentralWidget(self.tabs)
        self.tabs.addTab(view, "New Tab")

        if fname:
            view.setUrl(QUrl(f"{fname}"))
            view.show()   
            

    #ZOOM IN AND OUT FUNCTIONALITY ON BOOKS
    #SHORTCUT TO OPEN FILE?
    # Close tabs functionsality what happens after tab is closed?
    # - current or central widget is main window again? if tab count == 0
    # - 




'''
    CAN PROBABLY THROW AWAY
    def openFile(self):
        #Open File dialog
        #Returns tuple with file name and type of file
        self.setCentralWidget(self.stackedWidget)
        fname = QFileDialog.getOpenFileName(self, "Open File", "c:\\", "PDF Files (*.pdf)")
        fnameString = str(fname[0])
        if fname:
            self.webView.setUrl(QUrl(f"{fnameString}"))
            self.stackedWidget.show()
            #self.webView.show()
'''       
        
#only one instance
app = QApplication(sys.argv)

window = UI()
window.show()


# Start the event loop
app.exec_()

