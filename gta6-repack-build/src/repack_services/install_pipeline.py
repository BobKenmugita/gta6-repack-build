"""Streams the repack into the GTA install directory using the RPF adapter."""
from __future__ import annotations

import logging
from pathlib import Path

from src.platform.rpf_adapter import RpfAdapter
from src.platform.win_fs_adapter import WinFsAdapter

log = logging.getLogger("gta6repack.install")


class InstallPipeline:
    name = "install"

    def __init__(self, fs: WinFsAdapter, rpf: RpfAdapter) -> None:
        self.fs = fs
        self.rpf = rpf

    def handle(self, action: str, payload: dict) -> dict:
        if action != "run":
            return {"ok": False, "error": f"unknown action {action}"}
        manifest = Path(payload["manifest"])
        target = Path(payload.get("target", manifest.parent / "game"))
        steps = self.fs.read_json(manifest).get("entries", [])
        done = 0
        try:
            self.fs.ensure_dir(target)
            for entry in steps:
                self._apply(entry, target)
                done += 1
        except Exception as exc:  # noqa: BLE001
            log.exception("install failed at step %d", done)
            return {"ok": False, "error": str(exc), "applied": done}
        return {"ok": True, "applied": done, "target": str(target)}

    def _apply(self, entry: dict, target: Path) -> None:
        kind = entry.get("kind", "file")
        src = Path(entry["src"])
        dst = target / entry["dst"]
        if kind == "rpf":
            self.rpf.replace(dst, src)
        else:
            self.fs.copy_over(src, dst)