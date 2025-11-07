from PySide6.QtWidgets import (
    QWidget, QMainWindow, QLabel,
    QHBoxLayout, QVBoxLayout, QFrame
)
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt

from .sidebar import SideBar
from .topbar import TopBar
from .cards import StatCards
from .chart import LineChartWidget
from .table import SensorTable

from ..data.mock import sensor_kpis


class MainWindow(QMainWindow):
    def __init__(self, store, i18n):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setMinimumSize(1200, 800)

        self.store = store
        self.i18n = i18n

        # Root container
        container = QWidget()
        root = QHBoxLayout(container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar (left)
        self.sidebar = SideBar(self.store, self.i18n)
        root.addWidget(self.sidebar)

        # Right panel
        right = QWidget()
        right.setObjectName("RightPane")
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(40, 30, 40, 30)
        right_l.setSpacing(22)

        # Top filters bar
        self.topbar = TopBar(self.store, self.i18n)
        right_l.addWidget(self.topbar)

        # Dashboard title
        self.title = QLabel(self.i18n.t("dashboard.title"))
        self.title.setObjectName("H1")
        right_l.addWidget(self.title)

        # KPI Cards
        self.cards = StatCards(self.i18n)
        right_l.addWidget(self.cards)

        # ============ CHART + MEASUREMENTS SIDE BY SIDE ============
        chart_and_measures = QHBoxLayout()
        chart_and_measures.setSpacing(20)

        # Chart (bigger)
        self.chart = LineChartWidget()
        self.chart.setMinimumHeight(250)
        chart_and_measures.addWidget(self.chart, 6)  # 75%

        # Measurements card
        self.measurements = QFrame()
        self.measurements.setObjectName("Card")
        m_l = QVBoxLayout(self.measurements)
        m_l.setContentsMargins(24, 24, 24, 24)
        m_l.setSpacing(14)

        title_m = QLabel("Measurements")
        title_m.setStyleSheet("font-weight: 600; font-size: 16px;")
        m_l.addWidget(title_m)

        # Mocked measurement values
        for text in [
            "1.02 cP — Viscosity",
            "25 °C — Temperature",
            "998 g/cc — Density",
            "1.2 bar — Pressure"
        ]:
            item = QLabel(text)
            item.setStyleSheet("font-size: 14px;")
            m_l.addWidget(item)

        chart_and_measures.addWidget(self.measurements, 2)  # 25%

        right_l.addLayout(chart_and_measures)

        # ============ Sensor Table (goes UNDER chart + measurements) ============
        self.sensor_table = SensorTable(
            self.i18n.t("dashboard.sensor_table")
        )
        right_l.addWidget(self.sensor_table)

        # Add right panel to root
        root.addWidget(right, 1)
        self.setCentralWidget(container)

        # Center window on screen
        screen = QScreen.availableGeometry(self.screen())
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

        # Load initial data
        self._load_data()

        # Re-render when store changes
        self.store.subscribe(self._on_state_change)

    # Load KPI values + chart data
    def _load_data(self):
        data = sensor_kpis()
        self.cards.set_values(data["data"], data["connected"], data["events"])
        self.chart.set_series(
            data["trend_data_this_year"],
            data["trend_data_last_year"]
        )

    def _on_state_change(self):
        self.title.setText(self.i18n.t("dashboard.title"))
        self.topbar.refresh_texts()
        self.sidebar.refresh_texts()
