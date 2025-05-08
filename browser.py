import sys
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton ,QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtGui
from PyQt5.QtCore import QUrl
 


class Local_Web_Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Local Web Browser"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 300
        self.iconName = "home"
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.UiComponents()

        self.show()

    def UiComponents(self):
         self.searchbar = QLineEdit()
         self.searchbar.setPlaceholderText("enter a query")
         self.search_button = QPushButton("search")
         self.search_button.clicked.connect(self.perform_search)

         self.browser = QWebEngineView()


         layout = QVBoxLayout()
         layout.addWidget(self.searchbar)
         layout.addWidget(self.search_button)
         layout.addWidget(self.browser)

         container = QWidget()
         container.setLayout(layout)
         self.setCentralWidget(container)

    def perform_search(self):
         query = self.searchbar.text().strip()
         if not query:
              return

         local_url = f"http://127.0.0.1:8085/{query}.html"

         try:
              response = requests.get(local_url)
              if response.status_code == 200:
                   self.browser.load(QUrl(local_url))
              else:
                   self.show_page_not_found(query)
         except requests.exceptions.ConnectionError: 
              self.show_page_not_found(query)

    def show_page_not_found(self, query):
         html =f"""
         <html>
         <html><title>No Such Document Found</title></head>
         <body>
             <h2>Document '{query}' not found locally.</h2>
             <p>try searching externally:</p>
             <ul>
                 <li><a href = 'http://www.google.com/search?q={query}'>search on google</a></li>
                 <li><a href ='http://www.bing.com/search?q={query}'>seach on bing</a></li>
             </ul>
          </body>
          </html>
          """
         self.browser.setHtml(html)                       

if __name__ =="__main__":
        App = QApplication(sys.argv)
        window = Local_Web_Browser()
        window.resize(600, 700)
        window.show()
        sys.exit(App.exec())    