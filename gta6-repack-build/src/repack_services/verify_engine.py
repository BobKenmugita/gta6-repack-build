"""Checks an installed GTA6 repack against the shipped SHA-256 table."""
from __future__ import annotations

import hashlib
from pathlib import Path

from src.platform.win_fs_adapter import WinFsAdapter


class VerifyEngine:
    name = "verify"

    def __init__(self, fs: WinFsAdapter) -> None:
        self.fs = fs

    def handle(self, action: str, payload: dict) -> dict:
        if action != "check":
            return {"ok": False, "error": f"unknown action {action}"}
        install_dir = Path(payload["install_dir"])
        table = self.fs.read_json(install_dir / "repack.sha256.json")
        bad: list[str] = []
        for rel, expected in table.items():
            digest = self._digest(install_dir / rel)
            if digest != expected:
                bad.append(rel)
        return {"ok": not bad, "mismatches": bad, "checked": len(table)}

    @staticmethod
    def _digest(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()