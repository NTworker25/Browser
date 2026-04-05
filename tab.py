from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.tabBar().setExpanding(True)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        # self.browser.urlChanged.connect(self.update_url_bar)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)


