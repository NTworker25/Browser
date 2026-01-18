import sys
from operator import index

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QPushButton, QLineEdit, QToolButton, QWidget, \
    QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QHBoxLayout
from styles import toolbar_styles, URL_BAR_STYLE


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        nav_bar = QWidget()
        self.full_url = ""
        nav_layout = QHBoxLayout(nav_bar)
        nav_bar.setFixedHeight(50)

        back_btn = QPushButton("←")
        back_btn.clicked.connect(self.browser.back)
        reset_btn = QPushButton("↻")
        reset_btn.clicked.connect(self.browser.reload)
        forward_btn = QPushButton("→")
        forward_btn.clicked.connect(self.browser.forward)
        # nav_layout.setStyleSheet(toolbar_styles)
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(reset_btn)
        nav_layout.addWidget(forward_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet(URL_BAR_STYLE)
        self.url_bar.returnPressed.connect(self. navigate_to_url)
        nav_layout.addWidget(self.url_bar)
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(nav_bar, 0)  # Панель навигации с stretch=0 (не растягивается)
        central_layout.addWidget(self.browser, 1)  # Браузер с stretch=1 (занимает всё оставшееся пространство)

        self.setCentralWidget(central_widget)

        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        full_url_text = self.url_bar.text()
        if not full_url_text.startswith("http"):
            full_url_text = "https://" + full_url_text
        url = QUrl(full_url_text)
        # print(type(url)) # <class QUrl>
        if not url.isValid():
            print(f"Ошибка: неверный URL {full_url_text}")
            return
        self.browser.setUrl(url)

    def make_beautiful_url(self, url_text: str) -> str:
        url_text = url_text[0:url_text.index("?")]
        qurl = QUrl(url_text)
        host = qurl.host()
        return host

    def update_url_bar(self, new_url: QUrl) -> None:
        self.full_url = new_url.toString()
        if not self.url_bar.hasFocus():
            short_url = self.make_beautiful_url(self.full_url)
            self.url_bar.setText(short_url)
        else:
            self.url_bar.setText(self.full_url)


app = QApplication(sys.argv)
main_window = Browser()
main_window.show()
sys.exit(app.exec_())
