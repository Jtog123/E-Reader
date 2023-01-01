from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

import sys
import os



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Get size of screen if needed
        screen = QApplication.primaryScreen()
        self.screenSize = screen.availableGeometry()

        #Set size of the window
        width = 800
        height = 800
        self.setMinimumSize(width, height)
        self.initUI()
        self.pageStack.currentChanged.connect(self.set_button_state)
        self.dictButton.clicked.connect(self.dictionary_page)
        self.readerButton.clicked.connect(self.reader_page)

    def initUI(self):

    
        #need to be class variable or local?
        self.button_action = QAction(QIcon('icons/folder-horizontal-open.png'), 'Open File', self)
        self.button_action.triggered.connect(self.readFile)
        self.button_action.setShortcut( QKeySequence("Ctrl+o") )


        #Create menu bar at top of screen
        self.menu = self.menuBar()
        fileMenu = self.menu.addMenu('&File')
        fileMenu.addAction(self.button_action)

        #dictionary takes place in side window?
        #Click on dict take me to another page?
        #How do i get back?
        dictionary = self.menu.addMenu('&Dictionary')
        

        #create button that opens file dialog
        self.button = QPushButton("&Open File", self)
        self.button.clicked.connect(self.readFile)
        self.button.move(0,200)

        ### footer buttons and widgets
        self.dictButton = QPushButton("&Dictionary",self)

        self.readerButton = QPushButton("&Reader",self)
        self.readerButton.setEnabled(False) #set to true when we click on dictionary button




        #Tab Widgets
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)

        #Close Tabs
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        #self.button.show() SHOW BUTTON AFTER TAB IS CLOSED?
        #Use event?

        #Corner tab button
        self.tabPlus = QToolButton(self)
        self.tabPlus.setText('+')
        self.tabs.setCornerWidget(self.tabPlus)
        self.tabPlus.clicked.connect(self.readFile)


        ###### ACTUALLY KIND OF WORKS

        #Layout allows for multiple widgets to be active at once
        #probably a good idea to set this up first before adding other widgets

        self.pageStack = QStackedWidget()

        mainLayout = QVBoxLayout()
        

        # Add the self.tabs widget and self.button to the layout
        mainLayout.addWidget(self.pageStack)
        #mainLayout.addWidget(self.tabs)
        self.pageStack.addWidget(self.tabs)
        #mainLayout.addWidget(self.button)
        #mainLayout.addWidget(self.dictButton)
        #layout.addStretch(0)

        #Footer
        footerWidget = QWidget()
        hLay = QHBoxLayout(footerWidget)
        hLay.addWidget(self.button, alignment=Qt.AlignLeft)
        hLay.addStretch()
        hLay.addWidget(self.readerButton, alignment=Qt.AlignRight)
        hLay.addWidget(self.dictButton,alignment=Qt.AlignRight)
        

        
    
        mainLayout.addWidget(footerWidget)
        

        # Create a widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(mainLayout)

        # Set the central widget of the main window to be the widget holding the layout
        self.setCentralWidget(central_widget)

    def set_button_state(self, index):
        print("vvv")

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

    def insert_page(self, index=-1):
        self.pageStack.insertWidget(index, QLabel("THis is page 2"))


    def dictionary_page(self):
        new_index = self.pageStack.currentIndex()+1
        if new_index < len(self.pageStack):
            self.pageStack.setCurrentIndex(new_index)        
        self.readerButton.setEnabled(True)

    def reader_page(self):
        new_index = self.pageStack.currentIndex()-1
        if new_index >= 0:
            self.pageStack.setCurrentIndex(new_index)



    #ZOOM IN AND OUT FUNCTIONALITY ON BOOKS
    #SHORTCUT TO OPEN FILE?
    # Adjust layout to liking
    #  Open new page when dictionary button is clicked
    #open to dictionary
    #go back to main page when reader button in clicked

#or inherit from Qmainwindow?
'''
Might now need
class DictionaryWindow(QWidget):
    def init(self):
        super(DictionaryWindow,self).__init__()
'''


        
if __name__ == '__main__':
    #only one instance
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.insert_page()


    # Start the event loop
    app.exec_()

