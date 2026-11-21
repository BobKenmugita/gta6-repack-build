"""Resolves a repack manifest into an ordered list of archive steps."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.repack_models.manifest_entry import ManifestEntry
from src.repack_models.repack_plan import RepackPlan
from src.platform.win_fs_adapter import WinFsAdapter


@dataclass
class ManifestResolver:
    fs: WinFsAdapter
    name: str = "manifest"

    def handle(self, action: str, payload: dict) -> dict:
        if action != "resolve":
            return {"ok": False, "error": f"unknown action {action}"}
        path = Path(payload["manifest"])
        try:
            entries = self._load(path)
        except FileNotFoundError:
            return {"ok": False, "error": f"manifest missing: {path}"}
        plan = RepackPlan(entries=entries, source=path)
        return {"ok": True, "plan": plan.to_dict(), "count": len(entries)}

    def _load(self, path: Path) -> list[ManifestEntry]:
        raw = self.fs.read_json(path)
        return [ManifestEntry.from_dict(e) for e in raw.get("entries", [])]