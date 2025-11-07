from typing import Callable, List


class Store:
    """Tiny pub/sub store for app settings and reactive updates."""

    def __init__(self):
        self._subs: List[Callable] = []
        self._language = "en"  # en|es
        self._collapsed = False

    # subscriptions
    def subscribe(self, cb: Callable):
        self._subs.append(cb)

    def _emit(self):
        for cb in self._subs:
            cb()

    # state slices
    @property
    def language(self):
        return self._language

    def set_language(self, lang: str):
        if lang in ("en", "es") and lang != self._language:
            self._language = lang
            self._emit()

    @property
    def sidebar_collapsed(self):
        return self._collapsed

    def toggle_sidebar(self):
        self._collapsed = not self._collapsed
        self._emit()
