from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class SideBar(QWidget):
    def __init__(self, store, i18n):
        super().__init__()
        self.store = store
        self.i18n = i18n
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)

        col = QVBoxLayout(self)
        col.setContentsMargins(20, 24, 16, 24)
        col.setSpacing(12)

        # Header button
        self.btn_toggle = QPushButton("Rheonics")
        self.btn_toggle.setObjectName("Ghost")
        import webbrowser
        self.btn_toggle.clicked.connect(lambda: webbrowser.open("https://rheonics.com/"))
        col.addWidget(self.btn_toggle)

        # Primary nav
        self.btn_dashboard = self._nav_btn("nav.dashboard", None, True)
        self.btn_sensors = self._nav_btn("nav.sensors", None, True)
        col.addWidget(self.btn_dashboard)
        col.addWidget(self.btn_sensors)

        col.addStretch(1)

        # Secondary nav
        self.btn_help = self._nav_btn("nav.help", None, False)
        self.btn_account = self._nav_btn("nav.account", None, False)

        # LANG
        self.btn_lang = self._nav_btn("nav.language", None, False)
        self.btn_lang.clicked.connect(self._cycle_lang)

        # THEME button
        self.btn_theme = self._nav_btn("nav.theme", None, False)
        self.btn_theme.clicked.connect(self._toggle_theme)

        col.addWidget(self.btn_help)
        col.addWidget(self.btn_account)
        col.addWidget(self.btn_lang)
        col.addWidget(self.btn_theme)

        self._apply_texts()


    def _nav_btn(self, key: str, icon_name, primary: bool):
        btn = QPushButton(self.i18n.t(key))
        btn.setObjectName("NavPrimary" if primary else "NavSecondary")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty("_key", key)
        return btn


    def _apply_texts(self):
        mapping = [
            (self.btn_dashboard, "nav.dashboard"),
            (self.btn_sensors, "nav.sensors"),
            (self.btn_help, "nav.help"),
            (self.btn_account, "nav.account"),
            (self.btn_lang, "nav.language"),
            (self.btn_theme, "nav.theme"),
        ]

        for btn, key in mapping:
            full = self.i18n.t(key)
            btn.setProperty("_fulltext", full)

            if not self.store.sidebar_collapsed:

                if btn is self.btn_theme:
                    btn.setText("Light Mode" if self.store.theme == "light" else "Dark Mode")
                else:
                    btn.setText(full)


    def refresh_texts(self):
        self._apply_texts()


    def _toggle(self):
        self.store.toggle_sidebar()
        collapsed = self.store.sidebar_collapsed
        self.setFixedWidth(72 if collapsed else 240)

        for b in (
            self.btn_dashboard, self.btn_sensors,
            self.btn_help, self.btn_account,
            self.btn_lang, self.btn_theme
        ):
            full = b.property("_fulltext")
            b.setText("" if collapsed else full)


    def _cycle_lang(self):
        self.store.set_language("es" if self.store.language == "en" else "en")


    def _toggle_theme(self):
        self.store.toggle_theme()
        self._apply_texts()
