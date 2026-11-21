"""Windows filesystem adapter — long-path aware, atomic copies."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


class WinFsAdapter:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    @staticmethod
    def _long(p: Path) -> str:
        s = str(p)
        if os.name == "nt" and not s.startswith("\\\\?\\"):
            return "\\\\?\\" + s
        return s

    def ensure_dir(self, p: Path) -> None:
        os.makedirs(self._long(p), exist_ok=True)

    def read_json(self, p: Path) -> dict:
        with open(self._long(p), "r", encoding="utf-8") as fh:
            return json.load(fh)

    def write_json(self, p: Path, data: dict) -> None:
        self.ensure_dir(p.parent)
        tmp = p.with_suffix(p.suffix + ".tmp")
        with open(self._long(tmp), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        os.replace(self._long(tmp), self._long(p))

    def copy_over(self, src: Path, dst: Path) -> None:
        self.ensure_dir(dst.parent)
        shutil.copy2(self._long(src), self._long(dst))