import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QPushButton, QLineEdit, QToolButton, QWidget, \
    QVBoxLayout, QTabWidget
from PyQt5.QtCore import QUrl, QEvent, Qt
from PyQt5.QtWidgets import QHBoxLayout

from styles import toolbar_styles, URL_BAR_STYLE
from tab import TabWidget
from styles import TAB_WIDGET_STYLE


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("RobustBrowser")

        # tab_container = QWidget()
        # tab_container.setFixedHeight(50)
        # tabs_layout = QHBoxLayout(tab_container)

        new_tab_button = QPushButton("+")
        new_tab_button.setFixedSize(30, 30)

        self.tabs = QTabWidget()
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet(TAB_WIDGET_STYLE)
        self.setCentralWidget(self.tabs)
        self.tabs.setCornerWidget(new_tab_button, Qt.TopRightCorner)

        # tabs_layout.addWidget(self.tabs, 1)
        # tabs_layout.addWidget(new_tab_button)

        # Виждет вкладок
        self.add_new_tab()

    def add_new_tab(self):
        """Добавление новой вкладки"""

        tab = TabWidget()
        index = self.tabs.addTab(tab, "Новая вкладка")
        self.tabs.setCurrentIndex(index)
        tab.browser.titleChanged.connect(lambda title, idx=index: self.title_cut(idx, title, tab))

    def title_cut(self, idx: int, title: str, tab: TabWidget) -> None:
        """Обрезка названия вкладки"""

        if len(title) > 25:
            short_title = f"{title[:22]}..."
            self.tabs.setTabText(idx, short_title)
            self.tabs.setTabToolTip(idx, title)
            tab.tab_title = short_title
        else:
            self.tabs.setTabText(idx, title)
            tab.tab_title = title

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
