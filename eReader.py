from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

import sys
import os
import requests
import json

'''
TO DO
Apply multithreading?
'''


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
        self.init_ui()
        self.set_styles()

    def init_ui(self):

        #Opens file through using Tab, also includes shortcut for opening a file
        self.button_action = QAction(QIcon('icons/folder-horizontal-open.png'), 'Open File', self)
        self.button_action.triggered.connect(self.read_file)
        self.button_action.setShortcut( QKeySequence("Ctrl+o") )


        #Create menu bar at top of screen
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu('&File')
        file_menu.addAction(self.button_action)

        #Create view tab?

        #create button that opens file dialog
        self.open_file_button = QPushButton("&Open File", self)
        self.open_file_button.clicked.connect(self.read_file)
        


        #Dictionary Button toggle back and forth between reader
        self.dict_button = QPushButton("&Dictionary", self)
        self.dict_button.clicked.connect(self.dictionary_page)
        

        #Reader Button toggle back and forth between dictionary
        self.reader_button = QPushButton("&Reader", self)
        self.reader_button.setEnabled(False) #set to true when we click on dictionary button
        self.reader_button.clicked.connect(self.reader_page)

        self.search_button = QPushButton("&Search", self)
        self.search_button.clicked.connect(self.search_dict)

        #Search word label
        self.search_word_label = QLabel("")

        #Dictionary label
        self.dict_label = QLabel("Your search result will appear here.")
        self.dict_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.dict_label.setWordWrap(True)
        self.dict_font = QFont("Arial", 12, QFont.Bold)
        self.dict_label.setFont(self.dict_font)


        #Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)

        
        #Close Tabs
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)


        #Corner tab button
        self.tab_plus = QToolButton(self)
        self.tab_plus.setText('+')
        self.tab_plus.setStyleSheet("background-color:#c484a3")
        self.tabs.setCornerWidget(self.tab_plus)
        self.tab_plus.clicked.connect(self.read_file)

        #Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setText("Search")

        #Create the stackedwidget and the mainlayout which is a vertical box layout
        self.page_stack = QStackedWidget()
        main_layout = QVBoxLayout()


        # Create a central widget, set the layout as the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Make the windows central widget the central_widget variable
        self.setCentralWidget(central_widget)

        #Search Header Widget
        self.header_widget = QWidget()
        search_layout = QHBoxLayout(self.header_widget)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch()
        main_layout.addWidget(self.header_widget)
        self.header_widget.hide()
        

        #Add the stackedWidget to the mainlayout, add the tabswidget to the stackedwidget
        main_layout.addWidget(self.page_stack)
        self.page_stack.addWidget(self.tabs)


        #Footer Layout with buttons added
        footer_widget = QWidget()
        h_lay = QHBoxLayout(footer_widget)
        h_lay.addWidget(self.open_file_button, alignment=Qt.AlignLeft)
        h_lay.addStretch()
        h_lay.addWidget(self.reader_button, alignment=Qt.AlignRight)
        h_lay.addWidget(self.dict_button,alignment=Qt.AlignRight)

        
        #Add the footer widget to the main layout
        main_layout.addWidget(footer_widget)


    #Read files
    def read_file(self):
        f_name = QFileDialog.getOpenFileName(self, "Open File", "c:\\", "PDF Files (*.pdf)")
        f_name_string = str(f_name[0])
        if f_name_string != '':
            self.add_new_tab(f_name_string)
            
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
        self.page_stack.insertWidget(index, self.dict_label) #Might have to create own label

        
    def dictionary_page(self):
        self.header_widget.show()

        new_index = self.page_stack.currentIndex() + 1
        if new_index < len(self.page_stack):
            self.page_stack.setCurrentIndex(new_index)  

        self.reader_button.setEnabled(True)
        self.dict_button.setEnabled(False)
        self.open_file_button.setEnabled(False)


    def reader_page(self):
        self.header_widget.hide()

        new_index = self.page_stack.currentIndex() - 1
        if new_index >= 0:
            self.page_stack.setCurrentIndex(new_index)
        
        self.reader_button.setEnabled(False)
        self.dict_button.setEnabled(True)
        self.open_file_button.setEnabled(True)
    
    def search_dict(self):
        dictionary = Dictionary() #Create dict
        search_text = self.search_bar.text() #get text from bar

        if search_text != '':
            self.dict_label.setStyleSheet("color: black")
            self.dict_label.setStyleSheet("background-color: #dcdedc;")
            dictionary.update_url(search_text) #Update url with new search term
            self.dict_label.setText(search_text +": "+ "\n" + dictionary.recieved_definition)
        else:
            self.dict_label.setStyleSheet("color: red")
            self.dict_label.setText("Enter a valid word")
    
    def set_styles(self):
        self.setStyleSheet("background-color: #a2aba5;")
        self.menu.setStyleSheet("background-color: #c2c4c3;")
        self.open_file_button.setStyleSheet("background-color: #c2c4c3;")
        self.reader_button.setStyleSheet("background-color: #c2c4c3;")
        self.dict_button.setStyleSheet("background-color: #c2c4c3;")
        self.search_button.setStyleSheet("background-color: #c2c4c3;")
        self.search_bar.setStyleSheet("background-color: #c2c4c3;")
        self.dict_label.setStyleSheet("background-color: #dcdedc;")


class Dictionary():
    def __init__(self):

        self.app_id = os.environ.get("READER_ID") #YOUR API ID HERE
        self.app_key = os.environ.get("READER_API_KEY") # YOUR API KEY HERE
        self.language = "en-gb"
        self.search_word = "search"
        self.url = "https://od-api.oxforddictionaries.com:443/api/v2/words/" + self.language + "?q=" + self.search_word + "&fields=definitions"  
        self.request = requests.get(self.url, headers={"app_id": self.app_id, "app_key": self.app_key})
        self.data = self.request.json()
        self.recieved_definition = self.data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    
    def update_url(self, word):
        self.url = "https://od-api.oxforddictionaries.com:443/api/v2/words/" + self.language + "?q=" + word + "&fields=definitions" 
        self.update_request()
    
    def update_request(self):
        #Try catch here? if we make a bad request handle the exception. self.received definition equals. Not a word. Check spelling
        try:
            self.request = requests.get(self.url, headers={"app_id": self.app_id, "app_key": self.app_key})
            self.data = self.request.json()
            self.recieved_definition = self.data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        except KeyError:
            self.recieved_definition = "EXCEPTION THROWN: Potentially misspelled word, or word doesnt exist in dictionary." #Rephrase this

        
if __name__ == '__main__':
    #only one instance
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.insert_page()

    # Start the event loop
    app.exec_()

