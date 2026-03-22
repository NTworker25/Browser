from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabBar().setExpanding(True)

    def add_new_tab(self, qurl=None, label='Blank'):
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        self.web_engine = QWebEngineView()
        self.web_engine.setUrl(qurl)



