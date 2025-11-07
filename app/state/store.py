from typing import Callable, List


class Store:
    """Tiny reactive store for language + theme + sidebar state."""

    def __init__(self):
        self._subs: List[Callable] = []
        self._language = "en"
        self._collapsed = False
        self._theme = "light"  # light | dark

    # Subscriptions
    def subscribe(self, cb: Callable):
        self._subs.append(cb)

    def _emit(self):
        for cb in self._subs:
            cb()

    # ------------------ LANGUAGE ------------------
    @property
    def language(self):
        return self._language

    def set_language(self, lang: str):
        if lang in ("en", "es") and lang != self._language:
            self._language = lang
            self._emit()

    # ------------------ SIDEBAR --------------------
    @property
    def sidebar_collapsed(self):
        return self._collapsed

    def toggle_sidebar(self):
        self._collapsed = not self._collapsed
        self._emit()

    # ------------------ THEME ----------------------
    @property
    def theme(self):
        return self._theme

    def toggle_theme(self):
        self._theme = "dark" if self._theme == "light" else "light"
        self._emit()
