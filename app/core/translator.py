import json
from pathlib import Path


class I18N:
    def __init__(self, store):
        self.store = store
        base = Path(__file__).parent.parent / "i18n"
        with open(base / "en.json", "r", encoding="utf-8") as f:
            self.en = json.load(f)
        with open(base / "es.json", "r", encoding="utf-8") as f:
            self.es = json.load(f)

    def t(self, key: str) -> str:
        lang = self.store.language
        data = self.en if lang == "en" else self.es
        # simple dotted path lookup
        node = data
        for k in key.split("."):
            node = node.get(k, {}) if isinstance(node, dict) else {}
        return node if isinstance(node, str) else key
