from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QComboBox, QPushButton
from PySide6.QtCore import Qt


class TopBar(QWidget):
    def __init__(self, store, i18n):
        super().__init__()
        self.store = store
        self.i18n = i18n
        self.setObjectName("TopBar")
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        self.search = QLineEdit()
        self.search.setPlaceholderText(self.i18n.t("filters.search"))
        self.conn = QComboBox()
        self.conn.addItems(["USB", "Ethernet", "WiFi"])
        self.conn.setPlaceholderText(self.i18n.t("filters.connection"))
        self.type = QComboBox()
        self.type.addItems(["SRD", "DVM", "SRV", "DVP"])
        self.type.setPlaceholderText(self.i18n.t("filters.sensor_type"))
        self.add_btn = QPushButton(self.i18n.t("actions.add_sensor"))

        row.addWidget(self.search, 3)
        row.addWidget(self.conn, 1)
        row.addWidget(self.type, 1)
        row.addStretch(1)
        row.addWidget(self.add_btn)

    def refresh_texts(self):
        self.search.setPlaceholderText(self.i18n.t("filters.search"))
        self.conn.setPlaceholderText(self.i18n.t("filters.connection"))
        self.type.setPlaceholderText(self.i18n.t("filters.sensor_type"))
        self.add_btn.setText(self.i18n.t("actions.add_sensor"))
