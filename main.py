import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction, QLineEdit, QToolButton
from PyQt5.QtCore import QUrl
from pygame.display import update


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.browser.back)
        toolbar.setStyleSheet("""
        QToolBar {
        background-color: #fff;
        padding: 8px;
        font-size: 14px;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 8px;
        text-align: center;
        }
        
        QToolButton {
        background-color: #222;
        color: #fff;
        padding: 6px 12px;
        border: 1px solid #444;
        border-radius: 4px;
        min-width: 40px;
        text-align: center; 
        font-size: 20px;
        }
        
        QToolButton:hover {
        background-color: #333;
        border-color: #888;
        }
        
        QToolButton:pressed {
        background-color: #444;
        }
        """)
        toolbar.addAction(back_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("""
        QLineEdit {
        padding: 8px 16px;
        font-size: 18px;
        }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)
        self.setCentralWidget(self.browser)
        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url_text = self.url_bar.text()
        print(url_text)
        if not url_text.startswith("http"):
            url_text = "https://" + url_text
        url = QUrl(url_text)
        if not url.isValid():
            print(f"Ошибка: неверный URL {url_text}")
            return
        self.browser.setUrl(url)

    def update_url(self, new_url):
        self.url_bar.setText(new_url.toString())


app = QApplication(sys.argv)
main_window = Browser()
main_window.show()
sys.exit(app.exec_())
