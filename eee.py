import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setFixedSize(600, 600)

        self.webEngineView = QWebEngineView()

        button1 = QPushButton("CLICK")
        button1.setFixedSize(QSize(50, 80))
        button1.setStyleSheet("""background-color: red;""")
        button1.clicked.connect(self.clickme)

        button2 = QPushButton("CLICK")
        button2.setFixedSize(QSize(50, 80))

        button3 = QPushButton("CLICK")
        button3.setFixedSize(QSize(50, 80))

        title_widget = QWidget()
        hlay = QHBoxLayout(title_widget)
        hlay.addWidget(button1, alignment=Qt.AlignLeft)
        hlay.addStretch()
        hlay.addWidget(button2, alignment=Qt.AlignRight)
        hlay.addWidget(button3, alignment=Qt.AlignRight)

        footer_widget = QWidget()

        hlay2 = QGridLayout(footer_widget)
        hlay2.addWidget(QPushButton("Foo"), 0, 0)
        hlay2.addWidget(QLineEdit("Bar"), 1, 0, 1, 2)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vlayout = QVBoxLayout(central_widget)
        vlayout.addWidget(title_widget)
        vlayout.addWidget(self.webEngineView, stretch=1)
        vlayout.addWidget(footer_widget)

        self.loadPage()

    def loadPage(self):

        html = """
        <html style="width: 100%; height: 100%; margin: 0; padding: 0;">
        <body style="overflow: hidden; width: 100%; height: 100%; margin: 0; padding: 0; background-color: #E6E6FA;">
        
        </body>
        </html>"""

        self.webEngineView.setHtml(html)

    def clickme(self):
        print("clicked")


app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow {background-color:white}")
window = MainWindow()
window.show()
sys.exit(app.exec_())