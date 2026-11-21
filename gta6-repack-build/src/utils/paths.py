"""Path helpers shared across the desktop shell."""
from __future__ import annotations

from pathlib import Path


def game_root() -> Path:
    return Path.home() / "Documents" / "GTA6Repack"


def manifest_path(name: str = "repack.manifest.json") -> Path:
    return game_root() / name


def log_dir() -> Path:
    p = game_root() / "logs"
    p.mkdir(parents=True, exist_ok=True)
    return p