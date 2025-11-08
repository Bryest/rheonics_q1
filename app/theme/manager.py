from pathlib import Path
from PySide6.QtWidgets import QApplication

class ThemeManager:
    _ROOT = Path(__file__).resolve().parent  # app/theme/

    @staticmethod
    def load(theme_name: str) -> str:
        base_path = ThemeManager._ROOT / "base.qss"
        theme_path = ThemeManager._ROOT / f"{theme_name}.qss"  # "light.qss" o "dark.qss"

        if not base_path.exists():
            raise FileNotFoundError(f"Missing base.qss at {base_path}")
        if not theme_path.exists():
            raise FileNotFoundError(f"Missing theme file at {theme_path}")

        base_css = base_path.read_text(encoding="utf-8")
        theme_css = theme_path.read_text(encoding="utf-8")

        # Orden IMPORTANTE: primero base (medidas), luego tema (colores)
        return f"/* ---- BASE ---- */\n{base_css}\n\n/* ---- THEME ({theme_name}) ---- */\n{theme_css}"

    @staticmethod
    def apply(widget, theme_name: str):
        css = ThemeManager.load(theme_name)
        app = QApplication.instance()
        # Limpia antes para evitar residuos de estilos previos
        app.setStyleSheet("")
        app.setStyleSheet(css)

