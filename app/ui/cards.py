from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QSize


class HoverCard(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setObjectName("Card")
        self.setProperty("hoverable", True)
        col = QVBoxLayout(self)
        col.setContentsMargins(16, 12, 16, 12)
        small = QLabel(title)
        small.setObjectName("Small")
        big = QLabel(str(value))
        big.setObjectName("KPI")
        col.addWidget(small)
        col.addWidget(big)


class StatCards(QWidget):
    def __init__(self, i18n):
        super().__init__()
        self.i18n = i18n
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)
        self.c1 = HoverCard(self.i18n.t("kpi.data"), "0")
        self.c2 = HoverCard(self.i18n.t("kpi.connected"), "0")
        self.c3 = HoverCard(self.i18n.t("kpi.events"), "0")
        for c in (self.c1, self.c2, self.c3):
            row.addWidget(c)

    def set_values(self, data, connected, events):
        self.c1.layout().itemAt(1).widget().setText(f"{data:,}")
        self.c2.layout().itemAt(1).widget().setText(str(connected))
        self.c3.layout().itemAt(1).widget().setText(str(events))
