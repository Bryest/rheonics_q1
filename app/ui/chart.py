from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QLinearGradient, QColor, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChartTooltip(QWidget):
    """Floating tooltip like Figma: white box + border + text."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background: white;
            border-radius: 6px;
            border: 1px solid #DDD;
            padding: 6px 10px;
            font-size: 14px;
            font-weight: 600;
            color: #111;
        """)
        self.label = QLabel("0", self)
        self.label.setStyleSheet("background: transparent;")
        self.hide()

    def set_value(self, v):
        self.label.setText(f"{v:,}")
        self.adjustSize()


class LineChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.series_main = QLineSeries()
        self.series_alt = QLineSeries()

        # Pens
        pen_main = QPen(QColor("#222")); pen_main.setWidthF(2.2)
        self.series_main.setPen(pen_main)

        pen_alt = QPen(QColor("#6B8BB1")); pen_alt.setWidthF(2.0)
        pen_alt.setDashPattern([5, 4])
        self.series_alt.setPen(pen_alt)

        # Area under main line
        self.zero_series = QLineSeries()
        self.area = QAreaSeries(self.series_main, self.zero_series)
        grad = QLinearGradient(0, 0, 0, 1)
        grad.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        grad.setColorAt(0.0, QColor(0,0,0,25))
        grad.setColorAt(1.0, QColor(0,0,0,0))
        self.area.setBrush(QBrush(grad))
        self.area.setPen(Qt.NoPen)

        # Chart
        self.chart = QChart()
        self.chart.addSeries(self.area)
        self.chart.addSeries(self.series_main)
        self.chart.addSeries(self.series_alt)
        self.chart.legend().setVisible(True)

        # Hide area marker
        for m in self.chart.legend().markers(self.area):
            m.setVisible(False)

        # Axes
        self.axisX = QValueAxis()
        self.axisX.setLabelFormat("")
        self.axisX.setTickCount(12)

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
        self.view.mouseMoveEvent = self.on_mouse_move
        self.view.leaveEvent = self.on_mouse_leave

        # Tooltip overlay
        self.tooltip = ChartTooltip(self.view)
        self.last_x = None

        # Center layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    # ------------------------------------------------------------
    # Charge new series
    # ------------------------------------------------------------
    def set_series(self, a, b):
        self.series_main.clear()
        self.series_alt.clear()
        self.zero_series.clear()

        for i, v in enumerate(a, start=1):
            self.series_main.append(i, v)
            self.zero_series.append(i, 0)

        for i, v in enumerate(b, start=1):
            self.series_alt.append(i, v)

        # Update axis scale
        self.axisX.setRange(1, len(a))
        self.axisY.setRange(0, max(max(a), max(b)))

    #  Mouse move handler
    def on_mouse_move(self, event):
        pos = event.pos()
        chart_pos = self.chart.mapToValue(pos, self.series_main)

        x = chart_pos.x()
        if x < 1 or x > self.series_main.count():
            self.tooltip.hide()
            return

        index = int(round(x)) - 1
        if index < 0 or index >= self.series_main.count():
            return

        # Value from main series
        v = self.series_main.at(index).y()
        point = self.series_main.at(index)

        # Map to screen
        screen_point = self.chart.mapToPosition(point, self.series_main)

        # Tooltip
        self.tooltip.set_value(int(v))
        self.tooltip.move(screen_point.x() + 12, screen_point.y() - 20)
        self.tooltip.show()

        # Draw vertical line & circle (force repaint)
        self.last_x = screen_point.x()
        self.view.viewport().update()

    #  Hide tooltip al salir
    def on_mouse_leave(self, event):
        self.tooltip.hide()
        self.last_x = None
        self.view.viewport().update()

    # Draw vertical line + circle
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.last_x is None:
            return

        painter = QPainter(self.view.viewport())
        painter.setRenderHint(QPainter.Antialiasing)

        # Vertical line
        painter.setPen(QPen(QColor("#999"), 1.2))
        painter.drawLine(self.last_x, 10, self.last_x,
                         self.view.height() - 20)

        # Circle marker
        painter.setBrush(QColor("#FFF"))
        painter.setPen(QPen(QColor("#222"), 2))
        painter.drawEllipse(self.last_x - 5, self.tooltip.y() + 8, 10, 10)
