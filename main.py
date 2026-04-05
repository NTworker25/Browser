import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QPushButton, QLineEdit, QToolButton, QWidget, \
    QVBoxLayout, QTabWidget
from PyQt5.QtCore import QUrl, QEvent
from PyQt5.QtWidgets import QHBoxLayout

from styles import toolbar_styles, URL_BAR_STYLE
from tab import TabWidget


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.full_url = ""
        # self.browser = QWebEngineView()
        # self.browser.setUrl(QUrl("https://www.google.com"))
        # self.browser.urlChanged.connect(self.update_url_bar)

        # Настройки окна
        self.setGeometry(100, 100 , 1200, 800)
        self.setWindowTitle("RobustBrowser")

        # лейбл для кнопок навигации и поисковой строки
        # nav_bar = QWidget()
        # nav_bar.setFixedHeight(50)
        # nav_layout = QHBoxLayout(nav_bar)

        # Кнопки навигации
        # back_btn = QPushButton("←")
        # reset_btn = QPushButton("↻")
        # forward_btn = QPushButton("→")

        # Привязываем функции к кнопкам
        # back_btn.clicked.connect(self.browser.back)
        # reset_btn.clicked.connect(self.browser.reload)
        # forward_btn.clicked.connect(self.browser.forward)


        # Создание поисковой строки и получение событий
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet(URL_BAR_STYLE)
        self.url_bar.returnPressed.connect(self.validate_url)
        self.url_bar.installEventFilter(self)

        # Добавляем кнопки в виджет
        # nav_layout.addWidget(back_btn)
        # nav_layout.addWidget(reset_btn)
        # nav_layout.addWidget(forward_btn)
        # nav_layout.addWidget(self.url_bar)

        tab_container = QHBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        new_tab_button = QPushButton("+")
        new_tab_button.setFixedSize(30, 30)
        tab_container.addWidget(new_tab_button)
        # Создание окна
        # central_widget = QWidget()
        # central_layout = QVBoxLayout(central_widget)
        # central_layout.setContentsMargins(0, 0, 0, 0)
        # central_layout.setSpacing(0)
        # central_layout.addWidget(nav_bar, 0)  # Панель навигации с stretch=0 (не растягивается)
        # central_layout.addWidget(self.browser, 1)  # Браузер с stretch=1 (занимает всё оставшееся пространство)
        # # central_layout.addWidget(self.tab, 1)
        #
        # self.setCentralWidget(central_widget)

        # Виждет вкладок
        # tab_widgets = QTabWidget()
        self.add_new_tab()

    def add_new_tab(self):
        tab = TabWidget()
        index = self.tabs.addTab(tab, "Новая вкладка")
        self.tabs.setCurrentIndex(index)
        # if qurl is None:
        #     qurl = QUrl("https://www.google.com")
        # self.web_engine = QWebEngineView()
        # self.web_engine.setUrl(qurl)

    def close_tab(self, tab_index):
        if self.tabs.count() == 1:
            self.close()
        else:
            self.tabs.removeTab(index=tab_index)

    def validate_url(self) -> QUrl | None:
        full_url_text = self.url_bar.text()
        if not full_url_text.startswith("http"):
            full_url_text = "https://" + full_url_text
        url = QUrl(full_url_text)
        if not url.isValid():
            print(f'Ошибка: Неверный URL {url.toString()}')
            return None
        return url

    def go_to_url(self):
        url = self.validate_url()
        if url is None:
            return
        self.browser.setUrl(url)

    def cut_url(self, url_text: str) -> str:
        qurl = QUrl(url_text)
        if not qurl.isValid():
            return url_text
        host = qurl.host()
        if not host:
            return url_text
        parts = host.split('.')
        if len(parts) < 2:
            return host
        domain = '.'.join(parts[-2:])
        if len(parts) > 2:
            subdomain = '.'.join(parts[:-2])
            return f"{subdomain}.{domain}"
        else:
            return domain

    def update_url_bar(self, new_url: QUrl) -> None:
        self.full_url = new_url.toString()
        if not self.url_bar.hasFocus():
            short_url = self.cut_url(self.full_url)
            self.url_bar.setText(short_url)
        else:
            self.url_bar.setText(self.full_url)

    def eventFilter(self, obj, event):
        if obj == self.url_bar:
            if event.type() == QEvent.FocusIn:
                if self.full_url:
                    self.url_bar.setText(self.full_url)
            elif event.type() == QEvent.FocusOut:
                if self.full_url:
                    short_url = self.cut_url(self.full_url)
                    self.url_bar.setText(short_url)
        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Browser()
    main_window.show()
    sys.exit(app.exec_())
