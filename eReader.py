from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

import sys
import os
import requests
import json


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
        self.set_styles()

    def initUI(self):

        #Opens file through using Tab, also includes shortcut for opening a file
        self.button_action = QAction(QIcon('icons/folder-horizontal-open.png'), 'Open File', self)
        self.button_action.triggered.connect(self.readFile)
        self.button_action.setShortcut( QKeySequence("Ctrl+o") )


        #Create menu bar at top of screen
        self.menu = self.menuBar()
        fileMenu = self.menu.addMenu('&File')
        fileMenu.addAction(self.button_action)

        #Create view tab?

        #create button that opens file dialog
        self.openFilebutton = QPushButton("&Open File", self)
        self.openFilebutton.clicked.connect(self.readFile)
        


        #Dictionary Button toggle back and forth between reader
        self.dictButton = QPushButton("&Dictionary", self)
        self.dictButton.clicked.connect(self.dictionary_page)
        

        #Reader Button toggle back and forth between dictionary
        self.readerButton = QPushButton("&Reader", self)
        self.readerButton.setEnabled(False) #set to true when we click on dictionary button
        self.readerButton.clicked.connect(self.reader_page)

        self.searchButton = QPushButton("&Search", self)
        self.searchButton.clicked.connect(self.search_dict)

        #Search word label
        self.search_word_label = QLabel("")

        #Dictionary label
        self.dictLabel = QLabel("Your search result will appear here.")
        self.dictLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.dictLabel.setWordWrap(True)
        self.dictFont = QFont("Arial", 12, QFont.Bold)
        self.dictLabel.setFont(self.dictFont)


        #Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)

        
        #Close Tabs
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)


        #Corner tab button
        self.tabPlus = QToolButton(self)
        self.tabPlus.setText('+')
        self.tabPlus.setStyleSheet("background-color:#c484a3")
        self.tabs.setCornerWidget(self.tabPlus)
        self.tabPlus.clicked.connect(self.readFile)

        #Search Bar
        self.searchBar = QLineEdit()
        self.searchBar.setText("Search")

        #Create the stackedwidget and the mainlayout which is a vertical box layout
        self.pageStack = QStackedWidget()
        mainLayout = QVBoxLayout()


        # Create a central widget, set the layout as the main layout
        central_widget = QWidget()
        central_widget.setLayout(mainLayout)

        # Make the windows central widget the central_widget variable
        self.setCentralWidget(central_widget)

        #Search Header Widget
        self.headerWidget = QWidget()
        searchLayout = QHBoxLayout(self.headerWidget)
        searchLayout.addWidget(self.searchBar)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addStretch()
        mainLayout.addWidget(self.headerWidget)
        self.headerWidget.hide()
        

        #Add the stackedWidget to the mainlayout, add the tabswidget to the stackedwidget
        mainLayout.addWidget(self.pageStack)
        self.pageStack.addWidget(self.tabs)


        #Footer Layout with buttons added
        footerWidget = QWidget()
        hLay = QHBoxLayout(footerWidget)
        hLay.addWidget(self.openFilebutton, alignment=Qt.AlignLeft)
        hLay.addStretch()
        hLay.addWidget(self.readerButton, alignment=Qt.AlignRight)
        hLay.addWidget(self.dictButton,alignment=Qt.AlignRight)

        
        #Add the footer widget to the main layout
        mainLayout.addWidget(footerWidget)


    #Read files
    def readFile(self):
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

        self.tabs.addTab(view, "New Tab")

        #Figure out how to get pdf name as string
        if fname:
            view.setUrl(QUrl(f"{fname}"))
            view.show()

    def insert_page(self, index = -1):
        self.pageStack.insertWidget(index, self.dictLabel) #Might have to create own label

        
    def dictionary_page(self):
        self.headerWidget.show()

        new_index = self.pageStack.currentIndex() + 1
        if new_index < len(self.pageStack):
            self.pageStack.setCurrentIndex(new_index)  

        self.readerButton.setEnabled(True)
        self.dictButton.setEnabled(False)
        self.openFilebutton.setEnabled(False)


    def reader_page(self):
        self.headerWidget.hide()

        new_index = self.pageStack.currentIndex() - 1
        if new_index >= 0:
            self.pageStack.setCurrentIndex(new_index)
        
        self.readerButton.setEnabled(False)
        self.dictButton.setEnabled(True)
        self.openFilebutton.setEnabled(True)
    
    def search_dict(self):
        dictionary = Dictionary() #Create dict
        searchText = self.searchBar.text() #get text from bar

        if searchText != '':
            self.dictLabel.setStyleSheet("color: black")
            self.dictLabel.setStyleSheet("background-color: #dcdedc;")
            dictionary.update_url(searchText) #Update url with new search term
            self.dictLabel.setText(searchText +": "+ "\n" + dictionary.recievedDefinition)
        else:
            self.dictLabel.setStyleSheet("color: red")
            self.dictLabel.setText("Enter a valid word")
    
    def set_styles(self):
        self.setStyleSheet("background-color: #a2aba5;")
        self.menu.setStyleSheet("background-color: #c2c4c3;")
        self.openFilebutton.setStyleSheet("background-color: #c2c4c3;")
        self.readerButton.setStyleSheet("background-color: #c2c4c3;")
        self.dictButton.setStyleSheet("background-color: #c2c4c3;")
        self.searchButton.setStyleSheet("background-color: #c2c4c3;")
        self.searchBar.setStyleSheet("background-color: #c2c4c3;")
        self.dictLabel.setStyleSheet("background-color: #dcdedc;")


    #adjust names to be pythonic
    #Add zoom buttons
    #Threading?


class Dictionary():
    def __init__(self):

        self.app_id = os.environ.get("READER_ID") #YOUR API ID HERE
        self.app_key = os.environ.get("READER_API_KEY") # YOUR API KEY HERE
        self.language = "en-gb"
        self.searchWord = "search"
        self.url = "https://od-api.oxforddictionaries.com:443/api/v2/words/" + self.language + "?q=" + self.searchWord + "&fields=definitions"  
        self.request = requests.get(self.url, headers={"app_id": self.app_id, "app_key": self.app_key})
        self.data = self.request.json()
        self.recievedDefinition = self.data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    
    def update_url(self, word):
        self.url = "https://od-api.oxforddictionaries.com:443/api/v2/words/" + self.language + "?q=" + word + "&fields=definitions" 
        self.update_request()
    
    def update_request(self):
        #Try catch here? if we make a bad request handle the exception. self.received definition equals. Not a word. Check spelling
        try:
            self.request = requests.get(self.url, headers={"app_id": self.app_id, "app_key": self.app_key})
            self.data = self.request.json()
            self.recievedDefinition = self.data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        except KeyError:
            self.recievedDefinition = "EXCEPTION THROWN: Potentially misspelled word, or word doesnt exist in dictionary." #Rephrase this

        
if __name__ == '__main__':
    #only one instance
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.insert_page()

    # Start the event loop
    app.exec_()

