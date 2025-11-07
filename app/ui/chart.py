from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPen, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


# ──────────────────────────── Tooltip
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

    def set_value(self, v):
        self.label.setText(f"{v:,}")
        self.adjustSize()


# ──────────────────────────── Chart
class LineChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.series_main = QLineSeries()
        self.series_alt = QLineSeries()

        p1 = QPen(QColor("#222"))
        p1.setWidthF(2.4)
        self.series_main.setPen(p1)
        self.series_main.setName("This year")

        p2 = QPen(QColor("#6B8BB1"))
        p2.setDashPattern([5, 4])
        p2.setWidthF(2.0)
        self.series_alt.setPen(p2)
        self.series_alt.setName("Last year")

        # area
        self.zero_series = QLineSeries()
        self.area = QAreaSeries(self.series_main, self.zero_series)

        g = QLinearGradient(0,0,0,1)
        g.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        g.setColorAt(0, QColor(0,0,0,30))
        g.setColorAt(1, QColor(0,0,0,0))
        self.area.setBrush(QBrush(g))
        self.area.setPen(Qt.NoPen)

        self.chart = QChart()
        self.chart.addSeries(self.area)
        self.chart.addSeries(self.series_main)
        self.chart.addSeries(self.series_alt)

        # hide area marker
        for m in self.chart.legend().markers(self.area):
            m.setVisible(False)

        # axes
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

        # view
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setMouseTracking(True)
        self.view.viewport().setMouseTracking(True)

        # override
        self.view.mouseMoveEvent = self._mouse_move
        self.view.leaveEvent = self._mouse_leave

        # tooltip
        self.tooltip = ChartTooltip()
        self.chart.scene().addWidget(self.tooltip)

        self.crosshair_scene_x = None

        # layout
        box = QVBoxLayout(self)
        box.setContentsMargins(0,0,0,0)
        box.addWidget(self.view)


    # ──────────────────────────── load data
    def set_series(self, a, b):
        self.series_main.clear()
        self.series_alt.clear()
        self.zero_series.clear()

        for i, v in enumerate(a, start=1):
            self.series_main.append(i, v)
            self.zero_series.append(i, 0)

        for i, v in enumerate(b, start=1):
            self.series_alt.append(i, v)

        self.axisX.setRange(1, len(a))
        self.axisY.setRange(0, max(max(a), max(b)))


    # ──────────────────────────── Mouse handler (FIXED)
    def _mouse_move(self, event):
        # mouse → scene
        scene_pos = self.view.mapToScene(event.pos())

        value_pos = self.chart.mapToValue(scene_pos, self.series_main)

        x_val = value_pos.x()
        if x_val < 1 or x_val > self.series_main.count():
            self.tooltip.hide()
            self.crosshair_scene_x = None
            self.view.viewport().update()
            return

        idx = int(round(x_val)) - 1
        if idx < 0 or idx >= self.series_main.count():
            return

        point = self.series_main.at(idx)
        value = int(point.y())

        # data → chart pixel → scene → view
        pos_scene_point = self.chart.mapToScene(
            self.chart.mapToPosition(point, self.series_main)
        )
        pos_view = self.view.mapFromScene(pos_scene_point)

        # tooltip placement centered
        self.tooltip.set_value(value)
        self.tooltip.move(pos_view.x() - self.tooltip.width()//2,
                          pos_view.y() - 35)
        self.tooltip.show()

      
        self.crosshair_scene_x = pos_scene_point.x()
        self.view.viewport().update()


    def _mouse_leave(self, event):
        self.tooltip.hide()
        self.crosshair_scene_x = None
        self.view.viewport().update()


    # ──────────────────────────── Crosshair stamping
    def _paint_overlay(self, event):
        QChartView.paintEvent(self.view, event)  

        if self.crosshair_scene_x is None:
            return

        painter = QPainter(self.view.viewport())
        painter.setRenderHint(QPainter.Antialiasing)

        pt = self.view.mapFromScene(QPointF(self.crosshair_scene_x, 0))
        x = int(pt.x())

        painter.setPen(QPen(QColor("#999"), 1.4))
        painter.drawLine(x, 0, x, self.view.height())

        painter.setBrush(QColor("#FFF"))
        painter.setPen(QPen(QColor("#222"), 2))
        painter.drawEllipse(x - 5, self.tooltip.y() + 8, 10, 10)

