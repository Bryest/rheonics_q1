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

        # Search field
        self.search = QLineEdit()
        self.search.setPlaceholderText(self.i18n.t("filters.search"))

        # Connection dropdown
        self.conn = QComboBox()
        self.conn.addItems(["USB", "Ethernet", "WiFi"])
        self.conn.setEditable(False)

        # Replace label text via hidden dummy for accessibility
        self.conn.setProperty("placeholder", self.i18n.t("filters.connection"))

        # Sensor type dropdown
        self.type = QComboBox()
        self.type.addItems(["SRD", "DVM", "SRV", "DVP"])
        self.type.setEditable(False)
        self.type.setProperty("placeholder", self.i18n.t("filters.sensor_type"))

        # Add sensor button
        self.add_btn = QPushButton(self.i18n.t("actions.add_sensor"))
        self.add_btn.setObjectName("AddSensor")
        
        row.addWidget(self.search, 3)
        row.addWidget(self.conn, 1)
        row.addWidget(self.type, 1)
        row.addStretch(1)
        row.addWidget(self.add_btn)

    def refresh_texts(self):
        # Search placeholder
        self.search.setPlaceholderText(self.i18n.t("filters.search"))

        # Dropdown pseudo-placeholders
        self.conn.setProperty("placeholder", self.i18n.t("filters.connection"))
        self.type.setProperty("placeholder", self.i18n.t("filters.sensor_type"))

        # Add button
        self.add_btn.setText(self.i18n.t("actions.add_sensor"))
