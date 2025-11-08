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
from PySide6.QtWidgets import QSizePolicy

# ------------------------------------------------------------
# Helper: Measurement Row (value + pill)
# ------------------------------------------------------------
def make_measure_row(value_text: str, pill_text: str, pill_color: str):
    row = QFrame()
    layout = QVBoxLayout(row)
    layout.setContentsMargins(0, 0, 0, 12)
    layout.setSpacing(6)

    value = QLabel(value_text)
    value.setStyleSheet("font-size: 12px; color: #222;")
    layout.addWidget(value)

    pill = QLabel(pill_text)
    pill.setAlignment(Qt.AlignCenter)
    pill.setFixedHeight(32)
    pill.setStyleSheet(f"""
        background: {pill_color};
        border-radius: 10px;
        font-size: 14px;
        font-weight: 600;
        color: #444;
    """)
    layout.addWidget(pill)

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

        # Right Pane
        right = QWidget()
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(40, 30, 40, 30)
        right_l.setSpacing(22)

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

        # --------------------------- Responsive Layouts ---------------------------
        self.chart_layout_h = QHBoxLayout()
        self.chart_layout_h.setSpacing(20)

        self.chart_layout_v = QVBoxLayout()
        self.chart_layout_v.setSpacing(20)

        # Chart
        self.chart = LineChartWidget()
        self.chart.setMinimumHeight(320)

        # Measurements Card
        self.measurements = QFrame()
        self.measurements.setObjectName("Card")

        # FIX — evitar que se achique demasiado
        self.measurements.setMinimumHeight(360)
        self.measurements.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )

        m_l = QVBoxLayout(self.measurements)
        m_l.setContentsMargins(24, 24, 24, 24)
        m_l.setSpacing(16)

        # Title
        self.m_title = QLabel(self.i18n.t("kpi.measurements"))
        self.m_title.setStyleSheet("font-weight: 600; font-size: 16px;")
        m_l.addWidget(self.m_title)

        # Rows
        self.row_visc = make_measure_row("1.02 cP", self.i18n.t("kpi.viscosity"), "#F9D7D9")
        self.row_temp = make_measure_row("25 °C", self.i18n.t("kpi.temperature"), "#F6E8C3")
        self.row_dens = make_measure_row("998 g/cc", self.i18n.t("kpi.density"), "#D8EADF")
        self.row_pres = make_measure_row("1.2 bar", self.i18n.t("kpi.pressure"), "#DCD7F6")

        m_l.addWidget(self.row_visc)
        m_l.addWidget(self.row_temp)
        m_l.addWidget(self.row_dens)
        m_l.addWidget(self.row_pres)


        # Fill Horizontal layout
        self.chart_layout_h.setAlignment(Qt.AlignTop)
        self.chart_layout_h.addWidget(self.chart, 6)
        self.chart_layout_h.addWidget(self.measurements, 2)

        # Fill Vertical layout
        self.chart_layout_v.addWidget(self.chart)
        self.chart_layout_v.addWidget(self.measurements)

        # Start with Horizontal
        right_l.addLayout(self.chart_layout_h)
        self.current_layout = "H"

        # Sensor table
        self.sensor_table = SensorTable(
            self.i18n.t("dashboard.sensor_table"),
            self.i18n
        )
        right_l.addWidget(self.sensor_table)

        root.addWidget(right, 1)
        self.setCentralWidget(container)

        # Center Window
        screen = QScreen.availableGeometry(self.screen())
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )

        self._load_data()
        self.store.subscribe(self._on_state_change)

    # ------------------------------------------------------------
    # Load KPI / Chart
    # ------------------------------------------------------------
    def _load_data(self):
        data = sensor_kpis()
        self.cards.set_values(data["data"], data["connected"], data["events"])
        self.chart.set_series(
            data["trend_data_this_year"],
            data["trend_data_last_year"]
        )

    # ------------------------------------------------------------
    # Language Refresh
    # ------------------------------------------------------------
    def _on_state_change(self):
        self.title.setText(self.i18n.t("dashboard.title"))
        self.topbar.refresh_texts()
        self.sidebar.refresh_texts()
        self.cards.refresh_texts()
        self.sensor_table.refresh_header()

        self.m_title.setText(self.i18n.t("kpi.measurements"))

        self.row_visc.layout().itemAt(1).widget().setText(self.i18n.t("kpi.viscosity"))
        self.row_temp.layout().itemAt(1).widget().setText(self.i18n.t("kpi.temperature"))
        self.row_dens.layout().itemAt(1).widget().setText(self.i18n.t("kpi.density"))
        self.row_pres.layout().itemAt(1).widget().setText(self.i18n.t("kpi.pressure"))
