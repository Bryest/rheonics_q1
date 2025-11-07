from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor, QPainter


# ------------------------------------------------------------
# Status Tag
# ------------------------------------------------------------
class StatusTag(QLabel):
    def __init__(self, text: str, color: str):
        super().__init__(text)
        self.setObjectName("StatusTag")
        self.setProperty("tagColor", color)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(28)

        self.setStyleSheet("""
            QLabel#StatusTag {
                padding: 4px 12px;
                border-radius: 14px;
                font-size: 13px;
                font-weight: 500;
            }
            QLabel#StatusTag[tagColor="blue"]   { background: #E8F2FF; color: #125DCE; }
            QLabel#StatusTag[tagColor="green"]  { background: #E6F8EC; color: #2F8E4E; }
            QLabel#StatusTag[tagColor="gray"]   { background: #EBEBEB; color: #555; }
        """)


# ------------------------------------------------------------
# Toggle Switch
# ------------------------------------------------------------
class Toggle(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(42, 22)
        self.checked = False
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Background track
        track_color = "#4A90E2" if self.checked else "#D0D4DA"
        p.setBrush(QColor(track_color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 11, 11)

        # Knob
        knob_x = 20 if self.checked else 2
        p.setBrush(QColor("white"))
        p.drawEllipse(knob_x, 2, 18, 18)

    def mousePressEvent(self, event):
        self.checked = not self.checked
        self.update()


# ------------------------------------------------------------
# Edit Button
# ------------------------------------------------------------
class EditButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(32, 32)

        self.setIcon(QIcon("app/assets/edit.png"))
        self.setIconSize(QSize(20, 20))

        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background: #E8F2FF;
                border-radius: 6px;
            }
        """)


# ------------------------------------------------------------
# Utility wrapper for alignment
# ------------------------------------------------------------
def cell(widget, align=Qt.AlignLeft):
    w = QWidget()
    layout = QHBoxLayout(w)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(align)
    layout.addWidget(widget)
    return w


# ------------------------------------------------------------
# Table Row
# ------------------------------------------------------------
class TableRow(QFrame):
    def __init__(self, sensor, serial, status, color, shaded=False):
        super().__init__()

        self.setMinimumHeight(56)

        if shaded:
            self.setStyleSheet("background: #F4F6FA; border-radius: 10px;")
        else:
            self.setStyleSheet("background: transparent;")

        row = QHBoxLayout(self)
        row.setContentsMargins(20, 12, 20, 12)
        row.setSpacing(0)

        # SAME STRETCH FACTORS AS HEADER
        row.addWidget(cell(QLabel(sensor)), 2)
        row.addWidget(cell(QLabel(serial)), 3)
        row.addWidget(cell(StatusTag(status, color), Qt.AlignCenter), 2)

        # ACTION column now uses Toggle only
        row.addWidget(cell(Toggle(), Qt.AlignCenter), 2)

        # Edit icon
        row.addWidget(cell(EditButton(), Qt.AlignCenter), 1)


# ------------------------------------------------------------
# Table
# ------------------------------------------------------------
class SensorTable(QFrame):
    def __init__(self, title, i18n):
        super().__init__()
        self.i18n = i18n
        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # Title
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(self.lbl_title)

        # Header
        header = QHBoxLayout()
        header.setContentsMargins(20, 0, 20, 0)
        header.setSpacing(0)

        self.headers = {
            "sensor": QLabel(),
            "serial": QLabel(),
            "status": QLabel(),
            "action": QLabel(),
            "edit": QLabel()
        }

        header.addWidget(cell(self.headers["sensor"]), 2)
        header.addWidget(cell(self.headers["serial"]), 3)
        header.addWidget(cell(self.headers["status"], Qt.AlignCenter), 2)
        header.addWidget(cell(self.headers["action"], Qt.AlignCenter), 2)
        header.addWidget(cell(self.headers["edit"], Qt.AlignCenter), 1)

        layout.addLayout(header)
        self.refresh_header()

        # DATA ROWS
        layout.addWidget(TableRow("SRD", "SRD-000-AC00", "Logging", "blue", True))
        layout.addWidget(TableRow("DVM", "DVM-000-GG00", "Complete", "green", False))
        layout.addWidget(TableRow("SRV", "SRV-000-RT00", "Pending", "gray", True))
        layout.addWidget(TableRow("DVP", "DVP-000-WD00", "Logging", "blue", False))

    def refresh_header(self):
        self.lbl_title.setText(self.i18n.t("dashboard.sensor_table"))
        self.headers["sensor"].setText(self.i18n.t("table.sensor"))
        self.headers["serial"].setText(self.i18n.t("table.serial"))
        self.headers["status"].setText(self.i18n.t("table.status"))
        self.headers["action"].setText(self.i18n.t("table.action"))
        self.headers["edit"].setText(self.i18n.t("table.edit"))
