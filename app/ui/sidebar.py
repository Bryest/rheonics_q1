from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

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

       # Toggle collapse
        self.btn_toggle = QPushButton("Rheonics")
        self.btn_toggle.setObjectName("Ghost")
        # Make hamburger clickable to open website
        import webbrowser
        self.btn_toggle.clicked.connect(lambda: webbrowser.open("https://rheonics.com/"))
        col.addWidget(self.btn_toggle)

        # Primary nav
        self.btn_dashboard = self._nav_btn("nav.dashboard", icon_name=None, primary=True)
        self.btn_sensors = self._nav_btn("nav.sensors", icon_name=None, primary=True)
        col.addWidget(self.btn_dashboard)
        col.addWidget(self.btn_sensors)

        col.addStretch(1)

        # Secondary nav
        self.btn_help = self._nav_btn("nav.help", icon_name=None, primary=False)
        self.btn_account = self._nav_btn("nav.account", icon_name=None, primary=False)
        self.btn_lang = self._nav_btn("nav.language", icon_name=None, primary=False)
        self.btn_lang.clicked.connect(self._cycle_lang)

        col.addWidget(self.btn_help)
        col.addWidget(self.btn_account)
        col.addWidget(self.btn_lang)

        self._apply_texts()

    def _nav_btn(self, key: str, icon_name: str | None, primary: bool):
        btn = QPushButton(self.i18n.t(key))
        btn.setObjectName("NavPrimary" if primary else "NavSecondary")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setProperty("_fulltext", self.i18n.t(key))
        return btn

    def _apply_texts(self):
        for b, key in (
            (self.btn_dashboard, "nav.dashboard"),
            (self.btn_sensors, "nav.sensors"),
            (self.btn_help, "nav.help"),
            (self.btn_account, "nav.account"),
            (self.btn_lang, "nav.language"),
        ):
            txt = self.i18n.t(key)
            b.setProperty("_fulltext", txt)
            if not self.store.sidebar_collapsed:
                b.setText(txt)

    def refresh_texts(self):
        self._apply_texts()

    def _toggle(self):
        self.store.toggle_sidebar()
        collapsed = self.store.sidebar_collapsed
        self.setFixedWidth(72 if collapsed else 240)
        # hide/show texts
        for b in (self.btn_dashboard, self.btn_sensors, self.btn_help, self.btn_account, self.btn_lang):
            full = b.property("_fulltext")
            b.setText("" if collapsed else full)
        self.logo.setVisible(not collapsed)

    def _cycle_lang(self):
        self.store.set_language("es" if self.store.language == "en" else "en")
