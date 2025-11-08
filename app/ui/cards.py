from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


def _repolish(widget: QWidget) -> None:
    # Ensure QSS re-applies when dynamic properties change
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()


class HoverCard(QFrame):
    """Hoverable KPI card with theme-driven styles (#HoverCard)."""
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setObjectName("HoverCard")
        self.setProperty("hover", False)

        col = QVBoxLayout(self)
        col.setContentsMargins(16, 12, 16, 12)

        self.label_title = QLabel(title)
        self.label_title.setObjectName("KPI_Title")

        self.label_value = QLabel(str(value))
        self.label_value.setObjectName("KPI_Value")

        col.addWidget(self.label_title)
        col.addWidget(self.label_value)

    def enterEvent(self, event):
        self.setProperty("hover", True)
        _repolish(self)

    def leaveEvent(self, event):
        self.setProperty("hover", False)
        _repolish(self)


class StatCards(QWidget):
    """Three KPI cards row: Data / Connected / Events."""
    def __init__(self, i18n):
        super().__init__()
        self.i18n = i18n

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        self.c1 = HoverCard(self.i18n.t("kpi.data"), "0")
        self.c2 = HoverCard(self.i18n.t("kpi.connected"), "0")
        self.c3 = HoverCard(self.i18n.t("kpi.events"), "0")

        for card in (self.c1, self.c2, self.c3):
            row.addWidget(card)

    def set_values(self, data, connected, events):
        self.c1.label_value.setText(f"{data:,}")
        self.c2.label_value.setText(str(connected))
        self.c3.label_value.setText(str(events))

    def refresh_texts(self):
        self.c1.label_title.setText(self.i18n.t("kpi.data"))
        self.c2.label_title.setText(self.i18n.t("kpi.connected"))
        self.c3.label_title.setText(self.i18n.t("kpi.events"))
