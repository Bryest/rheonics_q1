import os


def load_stylesheet(theme: str) -> str:
    """
    Loads base.qss + the theme (light/dark) and returns a merged QSS string.
    """

    base_path = os.path.join("styles", "base.qss")
    # light.qss or dark.qss
    theme_path = os.path.join("styles", f"{theme}.qss")

    with open(base_path, "r") as f:
        base = f.read()

    with open(theme_path, "r") as f:
        colors = f.read()

    # base first, theme overrides
    return base + "\n\n" + colors
