# app/ui/table.py
from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor, QPainter, QBrush


class StatusTag(QLabel):
    """Small rounded label styled like Figma tags."""
    def __init__(self, text: str, color: str):
        super().__init__(text)
        self.setObjectName("StatusTag")
        self.setProperty("tagColor", color)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(26)
        self.setStyleSheet("""
            QLabel#StatusTag {
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 500;
            }
            QLabel#StatusTag[tagColor="blue"]   { background: #E8F2FF; color: #125DCE; }
            QLabel#StatusTag[tagColor="green"]  { background: #E6F8EC; color: #2F8E4E; }
            QLabel#StatusTag[tagColor="gray"]   { background: #EBEBEB; color: #555; }
        """)


class Toggle(QWidget):
    """Visual toggle only (no state changes)."""
    def __init__(self):
        super().__init__()
        self.setFixedSize(42, 22)
        self.checked = False
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QWidget {
                background: #D0D4DA;
                border-radius: 11px;
            }
        """)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # track
        track_color = QColor("#D0D4DA")
        p.setBrush(track_color)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 11, 11)

        # knob
        knob_color = QColor("#FFFFFF")
        x = 2 if not self.checked else 18
        p.setBrush(knob_color)
        p.drawEllipse(x, 2, 18, 18)

    def mousePressEvent(self, event):
        self.checked = not self.checked
        self.update()


class EditButton(QPushButton):
    """Blue edit button with pencil icon."""
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


class TableRow(QFrame):
    def __init__(self, sensor, serial, status, color, shaded=False):
        super().__init__()
        self.setObjectName("TableRow")

        # Minimum Height
        self.setMinimumHeight(48)

        # Background shading
        if shaded:
            self.setStyleSheet("border-radius: 12px;")
        else:
            self.setStyleSheet("background: transparent;")

        row = QHBoxLayout(self)
        # padding vertical
        row.setContentsMargins(16, 14, 16, 14)
        row.setSpacing(10)

        # column width behavior
        row.addWidget(QLabel(sensor), 2)
        row.addWidget(QLabel(serial), 3)
        row.addWidget(StatusTag(status, color), 2)
        row.addWidget(Toggle(), 1)
        row.addWidget(EditButton(), 1)



class SensorTable(QFrame):
    """The full Figma-style table block."""
    def __init__(self, title):
        super().__init__()
        self.setObjectName("Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # title
        lbl = QLabel(title)
        lbl.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(lbl)

        # header
        header = QHBoxLayout()
        for name in ["Sensor", "Serial number", "Status", "Action", "Edit"]:
            h = QLabel(name)
            h.setStyleSheet("color: #8A8F99; font-size: 14px;")
            header.addWidget(h, 1)
        layout.addLayout(header)

        # rows
        layout.addWidget(TableRow("SRD", "SRD-000-AC00", "Logging", "blue", shaded=True))
        layout.addWidget(TableRow("DVM", "DVM-000-GG00", "Complete", "green", shaded=False))
        layout.addWidget(TableRow("SRV", "SRV-000-RT00", "Pending", "gray", shaded=True))
        layout.addWidget(TableRow("DVP", "DVP-000-WD00", "Logging", "blue", shaded=False))
