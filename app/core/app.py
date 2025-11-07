from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from .translator import I18N
from ..state.store import Store
from ..ui.main_window import MainWindow
import sys


class RheonicsApp:
    def __init__(self):
        self.qt = QApplication(sys.argv)
        self.qt.setApplicationName("Prototype challenge Rheonics")
        self.store = Store()
        self.i18n = I18N(self.store)
        self.window = MainWindow(self.store, self.i18n)
        self.window.show()

    def run(self):
        sys.exit(self.qt.exec())
