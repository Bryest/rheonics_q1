from PySide6.QtWidgets import (
    QWidget, QMainWindow, QLabel,
    QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt

from .sidebar import SideBar
from .topbar import TopBar
from .cards import StatCards
from .chart import LineChartWidget
from .table import SensorTable
from ..data.mock import sensor_kpis

from app.theme.manager import ThemeManager


# ------------------------------------------------------------
# Measurement row factory
# ------------------------------------------------------------
def make_measure_row(value_text: str, pill_text: str, kind: str):
    row = QFrame()
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    value = QLabel(value_text)
    value.setObjectName("MeasureValue")
    value.setFixedWidth(70)
    value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    layout.addWidget(value)

    pill = QLabel(pill_text)
    pill.setObjectName("MeasurePill")
    pill.setProperty("kind", kind)
    pill.setAlignment(Qt.AlignCenter)
    pill.setFixedHeight(28)
    pill.setFixedWidth(120)
    layout.addWidget(pill)

    layout.addStretch()
    return row


# ------------------------------------------------------------
# Main Window
# ------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, store, i18n):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setMinimumSize(1200, 800)

        self.store = store
        self.i18n = i18n

        container = QWidget()
        root = QHBoxLayout(container)
        root.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = SideBar(self.store, self.i18n)
        root.addWidget(self.sidebar)

        # Right panel
        right = QWidget()
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(40, 30, 40, 30)

        # Top bar
        self.topbar = TopBar(self.store, self.i18n)
        right_l.addWidget(self.topbar)

        # Title
        self.title = QLabel(self.i18n.t("dashboard.title"))
        self.title.setObjectName("H1")
        right_l.addWidget(self.title)

        # KPI cards
        self.cards = StatCards(self.i18n)
        right_l.addWidget(self.cards)

        # Chart responsiveness
        self.chart_layout_h = QHBoxLayout()
        self.chart_layout_h.setSpacing(20)

        self.chart_layout_v = QVBoxLayout()
        self.chart_layout_v.setSpacing(20)

        # Chart
        self.chart = LineChartWidget(self.i18n)
        self.chart.setMinimumHeight(320)

        # Measurements card
        self.measurements = QFrame()
        self.measurements.setObjectName("Card")
        self.measurements.setMaximumWidth(300)
        self.measurements.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        m_l = QVBoxLayout(self.measurements)
        m_l.setContentsMargins(24, 24, 24, 24)
        m_l.setAlignment(Qt.AlignHCenter)

        self.m_title = QLabel(self.i18n.t("kpi.measurements"))
        self.m_title.setObjectName("H1")
        m_l.addWidget(self.m_title, 0, Qt.AlignHCenter)

        self.row_visc = make_measure_row("1.02 cP", self.i18n.t("kpi.viscosity"), "visc")
        self.row_temp = make_measure_row("25 °C", self.i18n.t("kpi.temperature"), "temp")
        self.row_dens = make_measure_row("998 g/cc", self.i18n.t("kpi.density"), "dens")
        self.row_pres = make_measure_row("1.2 bar", self.i18n.t("kpi.pressure"), "pres")

        m_l.addWidget(self.row_visc)
        m_l.addWidget(self.row_temp)
        m_l.addWidget(self.row_dens)
        m_l.addWidget(self.row_pres)

        # Layout H
        self.chart_layout_h.addWidget(self.chart, 6)
        self.chart_layout_h.addWidget(self.measurements, 2)

        # Layout V
        self.chart_layout_v.addWidget(self.chart)
        self.chart_layout_v.addWidget(self.measurements)

        right_l.addLayout(self.chart_layout_h)
        self.current_layout = "H"

        # ------------------------------------------------------------
        # ✅ TABLE CONTAINER (clean separation from chart)
        # ------------------------------------------------------------
        self.sensor_table = SensorTable(
            self.i18n.t("dashboard.sensor_table"), self.i18n
        )

        self.table_container = QFrame()
        self.table_container.setObjectName("TableContainer")

        table_layout = QVBoxLayout(self.table_container)
        table_layout.setContentsMargins(0, 35, 0, 0)  # top spacing from chart
        table_layout.addWidget(self.sensor_table)

        right_l.addWidget(self.table_container)

        # ------------------------------------------------------------

        root.addWidget(right, 1)
        self.setCentralWidget(container)

        # Center window
        screen = QScreen.availableGeometry(self.screen())
        self.move(screen.center().x() - self.width() // 2,
                  screen.center().y() - self.height() // 2)

        # Load data
        self._load_data()
        self.store.subscribe(self._on_state_change)
        self.apply_theme()

    # Theme application
    def apply_theme(self):
        qss = ThemeManager.load(self.store.theme)
        self.setStyleSheet(qss)

    # Responsive switch
    def resizeEvent(self, event):
        width = self.width()
        if width < 1100 and self.current_layout == "H":
            self._switch_to_vertical()
        elif width >= 1100 and self.current_layout == "V":
            self._switch_to_horizontal()
        super().resizeEvent(event)

    def _switch_to_vertical(self):
        parent = self.chart_layout_h.parent()
        parent.removeItem(self.chart_layout_h)
        parent.addLayout(self.chart_layout_v)
        self.current_layout = "V"

    def _switch_to_horizontal(self):
        parent = self.chart_layout_v.parent()
        parent.removeItem(self.chart_layout_v)
        parent.addLayout(self.chart_layout_h)
        self.current_layout = "H"

    # Load values
    def _load_data(self):
        data = sensor_kpis()
        self.cards.set_values(data["data"], data["connected"], data["events"])
        self.chart.set_series(data["trend_data_this_year"], data["trend_data_last_year"])

    # React to store changes
    def _on_state_change(self):
        self.title.setText(self.i18n.t("dashboard.title"))
        self.topbar.refresh_texts()
        self.sidebar.refresh_texts()
        self.cards.refresh_texts()
        self.sensor_table.refresh_header()

        self.chart.refresh_texts(self.i18n)

        self.m_title.setText(self.i18n.t("kpi.measurements"))
        self.row_visc.layout().itemAt(1).widget().setText(self.i18n.t("kpi.viscosity"))
        self.row_temp.layout().itemAt(1).widget().setText(self.i18n.t("kpi.temperature"))
        self.row_dens.layout().itemAt(1).widget().setText(self.i18n.t("kpi.density"))
        self.row_pres.layout().itemAt(1).widget().setText(self.i18n.t("kpi.pressure"))

        self.apply_theme()
