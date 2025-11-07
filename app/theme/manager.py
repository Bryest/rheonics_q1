from PySide6.QtCore import QFile, QTextStream

class ThemeManager:
    """Handles loading and applying theme stylesheets."""

    @staticmethod
    def load(theme_name: str):
        path = f"app/theme/{theme_name}.qss"
        file = QFile(path)

        if not file.open(QFile.ReadOnly | QFile.Text):
            print(f"Cannot load theme: {path}")
            return ""

        stream = QTextStream(file)
        return stream.readAll()
