from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


# ------------------------------------------------------------
# Tooltip (QSS themed, no inline CSS)
# ------------------------------------------------------------
class ChartTooltip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChartTooltip")

        self.label = QLabel("0", self)
        self.label.setObjectName("ChartTooltipLabel")

        self.hide()

    def set_value(self, v):
        self.label.setText(f"{v:,}")
        self.adjustSize()


# ------------------------------------------------------------
# Line Chart Widget (theme-driven)
# ------------------------------------------------------------
class LineChartWidget(QWidget):
    def __init__(self, i18n):
        super().__init__()
        self.setObjectName("ChartContainer")
        self.i18n = i18n

        # Title
        self.title = QLabel("")
        self.title.setObjectName("H1")
        self.title.setAlignment(Qt.AlignCenter)

        # Series
        self.series_main = QLineSeries()
        self.series_alt = QLineSeries()

        pen_main = QPen(QColor("#222"))
        pen_main.setWidthF(2.4)
        self.series_main.setPen(pen_main)

        pen_alt = QPen(QColor("#6B8BB1"))
        pen_alt.setDashPattern([5, 4])
        pen_alt.setWidthF(2.0)
        self.series_alt.setPen(pen_alt)

        # Area shading
        self.zero_series = QLineSeries()
        self.area = QAreaSeries(self.series_main, self.zero_series)

        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0, QColor(0, 0, 0, 30))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        self.area.setBrush(QBrush(gradient))
        self.area.setPen(Qt.NoPen)

        # Chart
        self.chart = QChart()
        self.chart.addSeries(self.area)
        self.chart.addSeries(self.series_main)
        self.chart.addSeries(self.series_alt)

        # Hide shaded legend marker
        for m in self.chart.legend().markers(self.area):
            m.setVisible(False)

        # Axes
        self.axisX = QValueAxis()
        self.axisX.setTickCount(12)
        self.axisX.setLabelFormat("")

        self.axisY = QValueAxis()
        self.axisY.setLabelFormat("%dK")

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        for s in (self.area, self.series_main, self.series_alt):
            s.attachAxis(self.axisX)
            s.attachAxis(self.axisY)

        # Chart view
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)
        self.view.viewport().setMouseTracking(True)

        # Chart frame (needed for QSS)
        self.chart_frame = QFrame()
        self.chart_frame.setObjectName("ChartFrame")

        frame_layout = QVBoxLayout(self.chart_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.view)

        # Tooltip
        self.tooltip = ChartTooltip()
        self.chart.scene().addWidget(self.tooltip)
        self.crosshair_scene_x = None

        # Events
        self.view.mouseMoveEvent = self._mouse_move
        self.view.leaveEvent = self._mouse_leave

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title)
        layout.addWidget(self.chart_frame)

        self.refresh_texts(self.i18n)

    # ------------------------------------------------------------
    # i18n
    # ------------------------------------------------------------
    def refresh_texts(self, i18n):
        self.i18n = i18n
        self.title.setText(self.i18n.t("chart.title"))
        self.series_main.setName(self.i18n.t("chart.var1"))
        self.series_alt.setName(self.i18n.t("chart.var2"))
        self.chart.legend().update()

    # ------------------------------------------------------------
    # Data
    # ------------------------------------------------------------
    def set_series(self, current, previous):
        self.series_main.clear()
        self.series_alt.clear()
        self.zero_series.clear()

        for i, v in enumerate(current, start=1):
            self.series_main.append(i, v)
            self.zero_series.append(i, 0)

        for i, v in enumerate(previous, start=1):
            self.series_alt.append(i, v)

        self.axisX.setRange(1, len(current))
        self.axisY.setRange(0, max(max(current), max(previous)))

    # ------------------------------------------------------------
    # Mouse event handlers
    # ------------------------------------------------------------
    def _mouse_move(self, event):
        scene_pos = self.view.mapToScene(event.pos())
        value_pos = self.chart.mapToValue(scene_pos, self.series_main)

        x_val = value_pos.x()
        if x_val < 1 or x_val > self.series_main.count():
            self.tooltip.hide()
            self.crosshair_scene_x = None
            self.view.viewport().update()
            return

        idx = int(round(x_val)) - 1
        point = self.series_main.at(idx)
        value = int(point.y())

        pos_scene = self.chart.mapToScene(
            self.chart.mapToPosition(point, self.series_main)
        )
        pos_view = self.view.mapFromScene(pos_scene)

        self.tooltip.set_value(value)
        self.tooltip.move(
            pos_view.x() - self.tooltip.width() // 2,
            pos_view.y() - 35
        )
        self.tooltip.show()

        self.crosshair_scene_x = pos_scene.x()
        self.view.viewport().update()

    def _mouse_leave(self, event):
        self.tooltip.hide()
        self.crosshair_scene_x = None
        self.view.viewport().update()
