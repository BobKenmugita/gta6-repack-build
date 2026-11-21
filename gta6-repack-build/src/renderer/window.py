"""Minimal Qt shell that drives the repack services via the bus."""
from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.main.repack_bus import RepackBus


class RepackWindow(QWidget):
    def __init__(self, bus: RepackBus) -> None:
        super().__init__()
        self.bus = bus
        self.setWindowTitle("GTA6 Repack — build launcher")
        self.resize(720, 480)

        self.status = QLabel("No manifest selected")
        self.log = QTextEdit(readOnly=True)
        pick = QPushButton("Select repack manifest…")
        go = QPushButton("Start install")

        pick.clicked.connect(self._pick)
        go.clicked.connect(self._install)

        lay = QVBoxLayout(self)
        lay.addWidget(self.status)
        lay.addWidget(pick)
        lay.addWidget(go)
        lay.addWidget(self.log)

    def _pick(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "repack.manifest.json", "", "*.json")
        if path:
            self.status.setText(path)
            self._manifest = path

    def _install(self) -> None:
        manifest = getattr(self, "_manifest", None)
        if not manifest:
            self.log.append("!! pick a manifest first")
            return
        result = self.bus.dispatch("install", "run", {"manifest": manifest})
        self.log.append(json.dumps(result, indent=2))