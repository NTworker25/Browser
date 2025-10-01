import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction, QLineEdit
from PyQt5.QtCore import QUrl


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.browser.back)
        toolbar.addAction(back_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)
        self.setCentralWidget(self.browser)

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


app = QApplication(sys.argv)
main_window = Browser()
main_window.show()
sys.exit(app.exec_())
