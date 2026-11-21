"""Thin wrapper around an external RPF archiver binary (OpenRPF-style CLI)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from src.platform.win_fs_adapter import WinFsAdapter


class RpfAdapter:
    BIN = "rpf-cli.exe"

    def __init__(self, fs: WinFsAdapter) -> None:
        self.fs = fs

    def available(self) -> bool:
        return shutil.which(self.BIN) is not None

    def replace(self, target_rpf: Path, payload: Path) -> None:
        if not self.available():
            raise RuntimeError("rpf-cli.exe not found on PATH")
        self.fs.ensure_dir(target_rpf.parent)
        subprocess.run(
            [self.BIN, "import", "--into", str(target_rpf), "--payload", str(payload)],
            check=True,
            capture_output=True,
        )