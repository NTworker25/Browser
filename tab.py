from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QUrl, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from styles import URL_BAR_STYLE


class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.tabBar().setExpanding(True)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.full_url = ""
        self.browser.urlChanged.connect(self.update_url_bar)

        # Создание поисковой строки и получение событий
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet(URL_BAR_STYLE)
        self.url_bar.returnPressed.connect(self.validate_url)
        self.url_bar.installEventFilter(self)

        # Лейбл для кнопок навигации и поисковой строки
        nav_bar = QWidget()
        nav_bar.setFixedHeight(50)
        nav_layout = QHBoxLayout(nav_bar)

        # Кнопки навигации
        back_btn = QPushButton("←")
        reset_btn = QPushButton("↻")
        forward_btn = QPushButton("→")

        # Привязываем функции к кнопкам
        back_btn.clicked.connect(self.browser.back)
        reset_btn.clicked.connect(self.browser.reload)
        forward_btn.clicked.connect(self.browser.forward)

        # Добавляем кнопки в виджет
        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(reset_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(self.url_bar)

        # Создание главного контейнера
        layout = QVBoxLayout()
        layout.addWidget(nav_bar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def validate_url(self) -> QUrl | None:
        """Валидация URL"""

        full_url_text = self.url_bar.text()
        if not full_url_text.startswith("http"):
            full_url_text = "https://" + full_url_text
        url = QUrl(full_url_text)
        if not url.isValid():
            print(f'Ошибка: Неверный URL {url.toString()}')
            return None
        return url

    def go_to_url(self):
        """Переход по текущей ссылке"""

        url = self.validate_url()
        if url is None:
            return
        self.browser.setUrl(url)

    def cut_url(self, url_text: str) -> str:
        """Обрезка URL"""

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
        """Записывает ссылку в интерфейс, отображение ссылки"""

        self.full_url = new_url.toString()
        if not self.url_bar.hasFocus():
            short_url = self.cut_url(self.full_url)
            self.url_bar.setText(short_url)
        else:
            self.url_bar.setText(self.full_url)

    def eventFilter(self, obj, event):
        """Перехватывает события url_bar и выполняет нужные действия"""

        if obj == self.url_bar:
            if event.type() == QEvent.FocusIn:
                if self.full_url:
                    self.url_bar.setText(self.full_url)
            elif event.type() == QEvent.FocusOut:
                if self.full_url:
                    short_url = self.cut_url(self.full_url)
                    self.url_bar.setText(short_url)
        return super().eventFilter(obj, event)
