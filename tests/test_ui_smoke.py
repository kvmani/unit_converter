from __future__ import annotations

from pathlib import Path
from html.parser import HTMLParser

import pytest

ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "units_converter" / "ui_dev"


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "link" and attrs_dict.get("rel") == "stylesheet":
            self.links.append(attrs_dict.get("href"))
        if tag == "script" and attrs_dict.get("type") == "module":
            self.scripts.append(attrs_dict.get("src"))


def test_ui_assets_exist():
    index = UI_DIR / "index.html"
    assert index.exists()
    parser = LinkCollector()
    parser.feed(index.read_text())
    for href in parser.links + parser.scripts:
        assert not href.startswith("http"), "External resources are not allowed"
        relative = href.lstrip("/")
        if relative.startswith("ui_dev/"):
            relative = relative.split("ui_dev/", 1)[1]
        target = UI_DIR / relative
        assert target.exists(), f"Missing asset: {href}"


def test_ui_structure():
    html = (UI_DIR / "index.html").read_text()
    assert "panel-left" in html
    assert "panel-center" in html
    assert "panel-right" in html
    assert "copy-buttons" in html
