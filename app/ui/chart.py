from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPen, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


# ──────────────────────────── Tooltip Widget
# A floating widget that displays the numeric value under the cursor.
class ChartTooltip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            background: white;
            border-radius: 8px;
            border: 1px solid #DDD;
            padding: 0px 12px;
            font-size: 14px;
            font-weight: 600;
        """)

        self.label = QLabel("0", self)
        self.label.setStyleSheet("background: transparent;")
        self.hide()

    # Update displayed value
    def set_value(self, v):
        self.label.setText(f"{v:,}")
        self.adjustSize()


# ──────────────────────────── Main LineChart Widget
class LineChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Main (current year) and alternative (last year) line series
        self.series_main = QLineSeries()
        self.series_alt = QLineSeries()

        # Main series styling
        p1 = QPen(QColor("#222"))
        p1.setWidthF(2.4)
        self.series_main.setPen(p1)
        self.series_main.setName("This year")

        # Alt series styling (dashed line)
        p2 = QPen(QColor("#6B8BB1"))
        p2.setDashPattern([5, 4])
        p2.setWidthF(2.0)
        self.series_alt.setPen(p2)
        self.series_alt.setName("Last year")

        # Area under the main line (for soft shading)
        self.zero_series = QLineSeries()        # always at Y=0 for area baseline
        self.area = QAreaSeries(self.series_main, self.zero_series)

        # Gradient fill from semi-transparent black → transparent
        g = QLinearGradient(0, 0, 0, 1)
        g.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        g.setColorAt(0, QColor(0, 0, 0, 30))
        g.setColorAt(1, QColor(0, 0, 0, 0))
        self.area.setBrush(QBrush(g))
        self.area.setPen(Qt.NoPen)

        # ───── Chart setup
        self.chart = QChart()
        self.chart.addSeries(self.area)
        self.chart.addSeries(self.series_main)
        self.chart.addSeries(self.series_alt)

        # Hide the legend item belonging to the shaded area series
        for m in self.chart.legend().markers(self.area):
            m.setVisible(False)

        # ───── Axis configuration
        self.axisX = QValueAxis()
        self.axisX.setTickCount(12)

        self.axisY = QValueAxis()
        self.axisY.setLabelFormat("%dK")

        # Attach axes to chart
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        # Bind each series to the axes
        for s in (self.area, self.series_main, self.series_alt):
            s.attachAxis(self.axisX)
            s.attachAxis(self.axisY)

        # ───── Chart view configuration
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)
        self.view.viewport().setMouseTracking(True)

        # Override event handlers for interactive tooltips + crosshair
        self.view.mouseMoveEvent = self._mouse_move
        self.view.leaveEvent = self._mouse_leave

        # Tooltip widget
        self.tooltip = ChartTooltip()
        self.chart.scene().addWidget(self.tooltip)

        # X coordinate of the vertical crosshair line (None = hidden)
        self.crosshair_scene_x = None

        # Layout container
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self.view)

    # ──────────────────────────── Load data into graph
    def set_series(self, a, b):
        self.series_main.clear()
        self.series_alt.clear()
        self.zero_series.clear()

        # Populate main and zero baseline series
        for i, v in enumerate(a, start=1):
            self.series_main.append(i, v)
            self.zero_series.append(i, 0)

        # Populate alt series
        for i, v in enumerate(b, start=1):
            self.series_alt.append(i, v)

        # Adjust axis ranges automatically
        self.axisX.setRange(1, len(a))
        self.axisY.setRange(0, max(max(a), max(b)))

    # ──────────────────────────── Mouse move handler
    # - Tracks cursor location
    # - Updates crosshair position
    def _mouse_move(self, event):
        # Convert mouse coords → chart scene coords
        scene_pos = self.view.mapToScene(event.pos())

        # Convert scene coords → chart values
        value_pos = self.chart.mapToValue(scene_pos, self.series_main)

        x_val = value_pos.x()
        # If cursor is outside data range, hide tooltip
        if x_val < 1 or x_val > self.series_main.count():
            self.tooltip.hide()
            self.crosshair_scene_x = None
            self.view.viewport().update()
            return

        # Get nearest index
        idx = int(round(x_val)) - 1
        if idx < 0 or idx >= self.series_main.count():
            return

        # Get exact data point
        point = self.series_main.at(idx)
        value = int(point.y())

        # Convert the data point coords back to pixel coordinates
        pos_scene_point = self.chart.mapToScene(
            self.chart.mapToPosition(point, self.series_main)
        )
        pos_view = self.view.mapFromScene(pos_scene_point)

        # Center the tooltip above the point
        self.tooltip.set_value(value)
        self.tooltip.move(
            pos_view.x() - self.tooltip.width() // 2,
            pos_view.y() - 35
        )
        self.tooltip.show()

        # Store x-position for vertical crosshair
        self.crosshair_scene_x = pos_scene_point.x()
        self.view.viewport().update()

    # ──────────────────────────── Mouse left chart area
    # Hide tooltip + crosshair
    def _mouse_leave(self, event):
        self.tooltip.hide()
        self.crosshair_scene_x = None
        self.view.viewport().update()
