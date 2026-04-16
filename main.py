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

        # Настройки окна
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("RobustBrowser")

        # tab_container = QWidget()
        # tabs_layout = QHBoxLayout(tab_container)
        # tabs_layout.setContentsMargins(0, 0, 0, 0)
        # tabs_layout.setSpacing(0)

        # new_tab_button = QPushButton("+")
        # new_tab_button.setFixedSize(30, 30)

        self.tabs = QTabWidget()
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # tabs_layout.addWidget(self.tabs, 1)
        # tabs_layout.addWidget(new_tab_button)

        # Создание окна
        # central_widget = QWidget()
        # central_layout = QVBoxLayout(central_widget)
        # central_layout.setContentsMargins(0, 0, 0, 0)
        # central_layout.setSpacing(0)
        # central_layout.addWidget(nav_bar, 0)  # Панель навигации с stretch=0 (не растягивается)
        # central_layout.addWidget(self.browser, 1)  # Браузер с stretch=1 (занимает всё оставшееся пространство)
        # central_layout.addWidget(self.tab, 1)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Browser()
    main_window.show()
    sys.exit(app.exec_())
